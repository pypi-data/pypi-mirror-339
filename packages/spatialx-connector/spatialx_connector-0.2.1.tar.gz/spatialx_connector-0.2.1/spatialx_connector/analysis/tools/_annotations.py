from typing import Optional, Literal

from ..._analysis import Analysis
from ..._anndata import ConnectorAnnData
from ..._constants import Species


def metadata_reference(
    adata: ConnectorAnnData,
    cluster_key: str,
    species: Literal[Species.HUMAN, Species.MOUSE],
    annotation_type: Literal["sub", "major"] = "sub",
    title: Optional[str] = None,
    **kwargs,
):
    """
    Spatial Region Segmentation.

    Parameters
    ----------
    cluster_key: `str`
        Cluster to predict cell types.
    species: `str`
        Species of data.
    annotation_type: `Literal["sub", "major"]`, Default: "sub"
        Type of annotation: Major or sub cell types.
    title: `Optional[str]`, Default: None
        Title of analysis, it will be used as name of embeddings.
        If not provided, a default name will be used.
    """
    analysis = adata.self_init(Analysis)
    analysis.prediction.metadata_reference(
        cluster_key=cluster_key,
        species=species,
        anno_type=annotation_type,
        title=title,
        info_args=adata._extend_information,
        **kwargs,
    )
    adata.update()
