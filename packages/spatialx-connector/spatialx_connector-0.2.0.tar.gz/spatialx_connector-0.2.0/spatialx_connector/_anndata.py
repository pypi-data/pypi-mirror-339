import os
import uuid
import logging
from tempfile import TemporaryDirectory
from functools import cached_property
from typing import List, Iterable, Collection, Tuple, Union, Optional

import zarr
import numpy as np
import pandas as pd
from scipy import sparse
from anndata import AnnData
from anndata._io.specs import read_elem
from anndata._core.file_backing import AnnDataFileManager
from anndata._core.aligned_mapping import AxisArrays, Layers, PairwiseArrays

from . import _constants as constants
from ._api import ZarrElement, OpenAPI, PyAPI
from ._analysis import Analysis


DEFAULT_LOGGER = logging.getLogger("spatialx_sdks_stdout")
SLICE = Union[int, slice, Collection]
SLICE_CHECK = (int, slice, Collection)


class AnnDataElement(ZarrElement):
    @cached_property
    def _data(self):
        return {}

    @cached_property
    def _parent(self):
        return self.self_init(ConnectorAnnData, os.path.dirname(self._path))

    def __setitem__(self, key: str, value):
        return super().__setitem__(key, value)

    def _get_mem_item(self, key: str):
        return self._data[key]

    def _get_item_iplm(self, key: str):
        return self.self_init(ZarrElement, path=os.path.join(self._path, key))

    def __getitem__(self, key: str):
        if key in self._data:
            return self._get_mem_item(key)

        key = self.get_id_by_name(key)
        return self._get_item_iplm(key)

    def keys(self):
        return np.unique(
            [k for k in sorted(self._name2id.keys()) if not k.startswith("AN-")] + list(self._data.keys())
        )

    def update(self):
        data = self._data
        new_obj: AnnDataElement = self.self_init(type(self))
        new_obj._data.update(data)
        return new_obj


class ConnectorDataFrame(AnnDataElement, AxisArrays):
    @cached_property
    def index_key(self):
        return self.attrs.get(
            constants.AnnDataKeys.INDEX_KEY.value,
            constants.AnnDataKeys.INDEX_KEY.value,
        )

    @cached_property
    def columns(self) -> List[str]:
        return [col for col in self.keys() if col != self.index_key]

    @cached_property
    def index(self):
        return pd.Index(read_elem(self.group[self.index_key]), name=self.index_key)

    def _get_mem_item(self, key: str):
        return pd.Series(
            self._data[key],
            index=self.index,
            name=self.get_name_by_id(key),
        )

    def _get_item_iplm(self, key: str):
        return pd.Series(
            read_elem(self.group[key]),
            index=self.index,
            name=self.get_name_by_id(key),
        )

    def __getitem__(self, keys: Union[str, List[str]]) -> pd.DataFrame:
        if isinstance(keys, list):
            return pd.concat([self[key] for key in keys], axis=1, keys=keys)
        return super().__getitem__(keys)

    def to_df(self) -> pd.DataFrame:
        """Convert to pandas DataFrame"""
        keys = [key for key in self.keys() if key != constants.AnnDataKeys.INDEX_KEY.value]
        if keys:
            return self[keys]
        return pd.DataFrame(index=self.index)

    @property
    def loc(self):
        return self.to_df().loc

    @property
    def iloc(self):
        return self.to_df().iloc


class ConnectorObs(ConnectorDataFrame):
    @property
    def _axis(self):
        return constants.AnnDataAxis.OBS.value


class ConnectorVar(ConnectorDataFrame):
    @property
    def _axis(self):
        return constants.AnnDataAxis.VAR.value


class ConnectorEmbeddings(AnnDataElement, AxisArrays):
    def _get_item_iplm(self, key: str):
        return self.group[key][:]


class ConnectorObsm(ConnectorEmbeddings):
    @property
    def _axis(self):
        return constants.AnnDataAxis.OBS.value


class ConnectorVarm(ConnectorEmbeddings):
    @property
    def _axis(self):
        return constants.AnnDataAxis.VAR.value


class ConnectorPairwiseArrays(AnnDataElement, PairwiseArrays):
    def _get_item_iplm(self, key: str):
        return read_elem(self.group[key])


class ConnectorObsp(ConnectorPairwiseArrays):
    @property
    def _axis(self):
        return constants.AnnDataAxis.OBS.value


class ConnectorVarp(ConnectorPairwiseArrays):
    @property
    def _axis(self):
        return constants.AnnDataAxis.VAR.value


class ConnectorCSCMatrix(AnnDataElement, sparse.csc_matrix):
    @property
    def data(self) -> zarr.Array:
        return self.group["data"]

    @property
    def indices(self) -> zarr.Array:
        return self.group["indices"]

    @property
    def indptr(self) -> zarr.Array:
        return self.group["indptr"]

    @cached_property
    def shape(self) -> tuple:
        return self.attrs["shape"]

    @property
    def major_axis(self):
        return 1

    @property
    def minor_axis(self):
        return 0

    def to_memory(self) -> sparse.csc_matrix:
        return sparse.csc_matrix(
            (self.data[:], self.indices[:], self.indptr[:]),
            shape=self.shape,
            dtype=self.data.dtype,
        )

    def __bulking_indices(self, indices: Collection) -> Tuple[Collection[Tuple[int, int]], np.ndarray]:
        seps = (np.diff(indices) != 1).nonzero()[0]
        indptr = np.empty(len(seps) + 2, dtype=np.int64)
        indptr[0] = 0
        indptr[1:-1] = seps + 1
        indptr[-1] = len(indices)
        segments = [
            (indices[s], indices[e - 1] + 1)
            for s, e in zip(indptr[:-1], indptr[1:])
        ]
        return segments, indptr

    def __get_index_from_slice(
        self, i: Union[SLICE, Tuple[SLICE, SLICE]], axis: int, max_len: int,
    ) -> Optional[np.ndarray]:
        ii = None
        if isinstance(i, Tuple) and len(i) > axis:
            ii = i[axis]
        elif isinstance(i, SLICE_CHECK) and axis == 0:
            ii = i

        if np.isscalar(ii):
            return np.array([ii], dtype=np.int32)
        if isinstance(ii, slice) and ii != slice(None):
            return np.arange(
                start=ii.start or 0,
                stop=ii.stop or max_len,
                step=ii.step,
                dtype=np.int32,
            )
        if isinstance(ii, Collection):
            return np.array(ii, dtype=np.int32)

        return None

    def _slice_major_axis(self, index: Iterable[int]) -> sparse.csc_matrix:
        indptr = np.empty(len(index) + 1, dtype=self.indptr.dtype)
        indptr[0] = 0
        indptr[1:] = np.diff(self.indptr)[index]
        indptr = np.cumsum(indptr, dtype=self.indptr.dtype)
        indices = np.empty(indptr[-1], dtype=self.indices.dtype)
        data = np.empty(indptr[-1], dtype=self.data.dtype)
        query_slices, query_indptr = self.__bulking_indices(index)
        for i, query_slice in enumerate(query_slices):
            dst_s = indptr[query_indptr[i]]
            dst_e = indptr[query_indptr[i + 1]]
            if dst_e == dst_s:
                continue
            src_s = self.indptr[query_slice[0]]
            src_e = self.indptr[query_slice[1]]
            data[dst_s: dst_e] = self.data[src_s: src_e]
            indices[dst_s: dst_e] = self.indices[src_s: src_e]

        shape = (self.shape[self.minor_axis], len(index))
        return sparse.csc_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

    def _slice_both_axes(self, col_idx: Iterable[int], row_idx: Iterable[int]) -> sparse.csc_matrix:
        data_arrs, indices_arrs = [], []
        indptr = np.zeros(len(col_idx) + 1, dtype=self.indptr.dtype)

        mask = np.zeros(self.shape[self.minor_axis], dtype=bool)
        mask[row_idx] = True

        for i, pos in enumerate(col_idx):
            s, e = self.indptr[pos], self.indptr[pos + 1]
            slice_data = self.data[s:e]
            slice_indices = self.indices[s:e]

            filtered_idx = mask[slice_indices]
            data_arrs.append(slice_data[filtered_idx])
            indices_arrs.append(slice_indices[filtered_idx])
            indptr[i + 1] = len(data_arrs[-1])

        indptr = np.cumsum(indptr)
        data = np.concatenate(data_arrs)
        indices = np.concatenate(indices_arrs)

        indices_mapping = np.zeros(self.shape[self.minor_axis], dtype=self.indices.dtype)
        indices_mapping[row_idx] = np.arange(len(row_idx), dtype=self.indices.dtype)
        indices = indices_mapping[indices]

        shape = (len(row_idx), len(col_idx))
        return sparse.csc_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

    def __getitem__(self, i: Union[SLICE, Tuple[SLICE, SLICE]]) -> sparse.csc_matrix:
        if not isinstance(i, tuple) and not isinstance(i, SLICE_CHECK):
            raise ValueError("Invalid slice")

        major_len = self.shape[self.major_axis]
        minor_len = self.shape[self.minor_axis]
        major_idx = self.__get_index_from_slice(i, self.major_axis, major_len)
        minor_idx = self.__get_index_from_slice(i, self.minor_axis, minor_len)

        if major_idx is None and minor_idx is None:
            return self.to_memory()

        if minor_idx is None:
            return self._slice_major_axis(major_idx)

        if len(minor_idx) != len(set(minor_idx)):
            raise ValueError("Minor axis slice on sparse matrix must be unique")

        major_idx = np.arange(self.shape[self.major_axis], dtype=np.int32) \
            if major_idx is None else major_idx

        res = self._slice_both_axes(major_idx, minor_idx)

        if len(major_idx) == 1 and len(minor_idx) == 1:
            res = res.toarray()[0][0]

        return res


class ConnectorAnnData(ZarrElement, AnnData):
    @cached_property
    def X(self) -> ConnectorCSCMatrix:
        return self.self_init(
            ConnectorCSCMatrix,
            os.path.join(self._path, constants.AnnDataAttr.X.value)
        )

    @cached_property
    def obs_names(self):
        return self.obs.index

    @cached_property
    def n_obs(self):
        return len(self.obs_names)

    @cached_property
    def var_names(self):
        return self.var.index

    @cached_property
    def n_vars(self):
        return len(self.var_names)

    def __repr__(self) -> str:
        descr = (
            f"{type(self).__name__} object with "
            f"n_obs × n_vars = {self.n_obs} × {self.n_vars}"
        )
        for attr in constants.AnnDataAttr:
            if attr.value not in self.group:
                continue
            if attr == constants.AnnDataAttr.X:
                continue
            keys = getattr(self, attr.value, {}).keys()
            if len(keys) > 0:
                descr += f"\n    {attr.value}: {str(list(keys))[1:-1]}"
        return descr

    def to_memory(self) -> AnnData:
        return AnnData(
            X=self.X.to_memory(),
            obs=self.obs.to_df(),
            var=self.var.to_df(),
            obsm={k: self.obsm[k] for k in self.obsm.keys()},
            varm={k: self.varm[k] for k in self.varm.keys()},
            obsp=self.obsp,
            varp=self.varp,
            layers=self.layers,
            uns=self.uns,
        )

    def copy(self) -> AnnData:
        return self.to_memory()

    @cached_property
    def _obs(self) -> ConnectorObs:
        return self.self_init(
            ConnectorObs,
            os.path.join(self._path, constants.AnnDataAttr.OBS.value)
        )

    @cached_property
    def _var(self) -> ConnectorVar:
        return self.self_init(
            ConnectorVar,
            os.path.join(self._path, constants.AnnDataAttr.VAR.value)
        )

    @cached_property
    def _obsm(self) -> ConnectorObsm:
        return self.self_init(
            ConnectorObsm,
            os.path.join(self._path, constants.AnnDataAttr.OBSM.value)
        )

    @cached_property
    def _varm(self) -> ConnectorVarm:
        return self.self_init(
            ConnectorVarm,
            os.path.join(self._path, constants.AnnDataAttr.VARM.value)
        )

    @cached_property
    def _obsp(self):
        return self.self_init(
            ConnectorObsp,
            os.path.join(self._path, constants.AnnDataAttr.OBSP.value)
        )

    @cached_property
    def _varp(self):
        return self.self_init(
            ConnectorVarp,
            os.path.join(self._path, constants.AnnDataAttr.VARP.value)
        )

    @cached_property
    def _raw(self):
        return None

    @cached_property
    def _layers(self):
        DEFAULT_LOGGER.warning("Create `layers` in memory.")
        return Layers(self)

    @cached_property
    def _uns(self):
        DEFAULT_LOGGER.warning("Create `uns` in memory.")
        return {}

    def _sanitize(self):
        DEFAULT_LOGGER.warning("[SKIP] Not support `_sanitize` function.")

    @property
    def filename(self):
        return None

    @cached_property
    def file(self):
        return AnnDataFileManager(self, None)

    @property
    def is_view(self):
        return False

    def upload_metadata(self, metadata: Union[pd.DataFrame, str, List[str]]):
        if isinstance(metadata, str):
            metadata = [metadata]
        if isinstance(metadata, list):
            metadata = self.obs[metadata]

        openapi: OpenAPI = self.self_init(OpenAPI)
        pyapi: PyAPI = self.self_init(PyAPI)
        with TemporaryDirectory(dir=".") as temp_dir:
            filename = f"{uuid.uuid4().hex}.tsv.gz"
            path = os.path.join(temp_dir, filename)
            metadata.to_csv(path, sep="\t")
            res = openapi.upload_file(
                file_path=path,
                folder_name="",
                upload_id=uuid.uuid4().hex,
                is_chunk=True,
            )
            csv_path = res[constants.ConnectorKeys.PATH.value]
            pyapi.import_metadata(
                study_id=self._extend_information[constants.ConnectorKeys.STUDY_ID.value],
                sample_id=self._extend_information[constants.ConnectorKeys.SAMPLE_ID.value],
                table_id=self._extend_information[constants.ConnectorKeys.TABLE_ID.value],
                csv_path=csv_path,
            )
        self.update()

    def upload_embeddings(self, embeddings: Union[str, List[str]]):
        if isinstance(embeddings, str):
            embeddings = [embeddings]
        adata = AnnData(
            X=sparse.csc_matrix((self.n_obs, 1)),
            obs=pd.DataFrame(index=self.obs_names),
            obsm={k: self.obsm[k] for k in embeddings}
        )

        openapi: OpenAPI = self.self_init(OpenAPI)
        analysis: Analysis = self.self_init(Analysis)
        with TemporaryDirectory(dir=".") as temp_dir:
            filename = f"{uuid.uuid4().hex}.h5ad"
            path = os.path.join(temp_dir, filename)
            adata.write_h5ad(path, compression="gzip")
            res = openapi.upload_file(
                file_path=path,
                folder_name="",
                upload_id=uuid.uuid4().hex,
                is_chunk=True,
            )
            h5ad_path = res[constants.ConnectorKeys.PATH.value]
            analysis.embeddings.upload_embeddings(h5ad_path, info_args=self._extend_information)
        self.update()

    def update(self):
        self._obs = self._obs.update()
        self._obsm = self._obsm.update()
        self._obsp = self._obsp.update()
        self._var = self._var.update()
        self._varm = self._varm.update()
        self._varp = self._varp.update()
