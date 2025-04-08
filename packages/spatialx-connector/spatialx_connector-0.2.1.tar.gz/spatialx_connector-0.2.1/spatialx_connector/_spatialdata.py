import os
import logging
from typing import List, Optional
from requests.auth import HTTPBasicAuth

from spatialdata._io.io_shapes import _read_shapes
from spatialdata._io.io_points import _read_points

from . import _constants as constants
from ._utils import time_cache
from ._api import Connector, ZarrElement, OpenAPI, PyAPI
from ._anndata import ConnectorAnnData


DEBUG_MODE = os.environ.get("DEBUG_MODE", "") == "TRUE"
DEFAULT_LOGGER = logging.getLogger("spatialx_sdks_stdout")


class Images(ZarrElement):
    def __getitem__(self, key: str):
        return self.group[self.get_id_by_name(key)]

    def get_channel_names(self, key: str):
        for attr in self[key].attrs.asdict().values():
            if isinstance(attr, dict) and constants.SpatialAttrs.CHANNELS_KEY.value in attr:
                return [
                    name[constants.SpatialAttrs.CHANNEL_LABEL.value]
                    for name in attr[constants.SpatialAttrs.CHANNELS_KEY.value]
                ]
        return []

    def set_channel_names(self, key: str, channel_names: List[str]):
        pyapi: PyAPI = self.self_init(PyAPI)
        return pyapi.rename_image_channels(
            self._extend_information[constants.ConnectorKeys.STUDY_ID.value],
            self._extend_information[constants.ConnectorKeys.SAMPLE_ID.value],
            self.get_id_by_name(key),
            channel_names,
        )


class Shapes(ZarrElement):
    def __getitem__(self, key: str):
        return _read_shapes(
            self._open_zarr_root(os.path.join(self._path, self.get_id_by_name(key)))
        )

    def simplify(self, key: str, tolerance: Optional[float]):
        pyapi: PyAPI = self.self_init(PyAPI)
        return pyapi.simplify_segmentation(
            self._extend_information[constants.ConnectorKeys.STUDY_ID.value],
            self._extend_information[constants.ConnectorKeys.SAMPLE_ID.value],
            self.get_id_by_name(key),
            tolerance,
        )


class Points(ZarrElement):
    def __getitem__(self, key: str):
        return _read_points(
            self._open_zarr_root(os.path.join(self._path, self.get_id_by_name(key)))
        )


class Tables(ZarrElement):
    def __getitem__(self, key: str):
        key = self.get_id_by_name(key)
        return self.self_init(
            ConnectorAnnData,
            path=os.path.join(self._path, key),
            extend_information={constants.ConnectorKeys.TABLE_ID.value: key},
        )


class SpatialData(Connector):
    def __init__(
        self,
        domain: str,
        token: str,
        data_id: Optional[str] = None,
        sample_id: Optional[str] = None,
        verify_ssl: bool = False,
        authentication: Optional[HTTPBasicAuth] = None,
    ):
        openapi = OpenAPI(domain, token, verify_ssl=verify_ssl, authentication=authentication)
        if sample_id is not None:
            details = openapi.get_sample_detail(sample_id)[constants.ConnectorKeys.SAMPLE.value]
            self.elements = None
        elif data_id is not None:
            details = openapi.get_sample_data_detail(data_id)

            submitted_elements: dict = details.get("map_submit_result", {})
            elements: List[str] = []
            for value in submitted_elements.values():
                if not isinstance(value, dict):
                    continue
                for v in value.values():
                    elements.extend(v.keys() if isinstance(v, dict) else [v])
            self.elements = elements

        self.study_id = details[constants.ConnectorKeys.STUDY_ID.value]
        self.sample_id = details[constants.ConnectorKeys.SAMPLE_ID.value]
        self.data_id = data_id
        study_path = openapi.get_study_detail(
            self.study_id
        )[constants.ConnectorKeys.STUDY.value][constants.ConnectorKeys.DATA_PATH.value]
        self._path = f"{study_path}/spatial/{self.sample_id}"

        super().__init__(
            domain, token,
            verify_ssl=verify_ssl,
            authentication=authentication,
        )

    def _init_attribute(self, Attribute, key: str):
        return self.self_init(
            Attribute,
            path=os.path.join(self._path, key),
            elements=self.elements,
            extend_information={
                constants.ConnectorKeys.DATA_ID.value: self.data_id,
                constants.ConnectorKeys.STUDY_ID.value: self.study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: self.sample_id,
            },
        )

    @property
    @time_cache(5)
    def images(self) -> Images:
        return self._init_attribute(Images, "images")

    @property
    @time_cache(5)
    def shapes(self) -> Shapes:
        return self._init_attribute(Shapes, "shapes")

    @property
    @time_cache(5)
    def points(self) -> Points:
        return self._init_attribute(Points, "points")

    @property
    @time_cache(5)
    def tables(self) -> Tables:
        return self._init_attribute(Tables, "table")

    def __repr__(self):
        obj_str = f"{type(self).__name__} with elements:"
        for key in ["images", "shapes", "points", "tables"]:
            element: ZarrElement = getattr(self, key)
            if len(element.keys()) == 0:
                continue
            obj_str += "\n\t" + element.repr()
        return obj_str
