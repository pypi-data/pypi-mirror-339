from typing import Optional

from ..._analysis import Analysis
from ..._anndata import ConnectorAnnData


def region_segmentation(
    adata: ConnectorAnnData,
    radius: float,
    mpp: float,
    species: str,
    resolution: float = 0.5,
    title: Optional[str] = None,
    **kwargs,
):
    """
    Spatial Region Segmentation.

    Parameters
    ----------
    radius: `float`
        Radius (micrometer) to build spatial graph
    mpp: `float`
        Micrometers per pixel.
    species: `str`
        Species of data.
    resolution : ``float``, Default: 0.5
        Resolution parameter, higher lead to more communities.
    title: `Optional[str]`, Default: None
        Title of analysis, it will be used as name of embeddings.
        If not provided, a default name will be used.
    """
    analysis = adata.self_init(Analysis)
    analysis.spatial_analysis.region_segmentation(
        radius=radius,
        mpp=mpp,
        species=species,
        resolution=resolution,
        title=title,
        info_args=adata._extend_information,
        **kwargs,
    )
