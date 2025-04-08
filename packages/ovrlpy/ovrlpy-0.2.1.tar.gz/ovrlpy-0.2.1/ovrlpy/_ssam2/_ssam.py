from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import tqdm

from .._patching import _patches, n_patches
from . import _utils
from ._utils import _TRUNCATE


def _sample_expression(
    coordinates: pd.DataFrame,
    kde_bandwidth: float = 2.5,
    minimum_expression: int = 2,
    min_pixel_distance: int = 5,
    coord_columns: Iterable[str] = ["x", "y", "z"],
    gene_column: str = "gene",
    n_workers: int = 8,
    mode: Optional[str] = None,
    patch_length: int = 500,
    dtype=np.float32,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Sample expression from a coordinate dataframe.

    Parameters
    ----------
        coordinates : Optional[pandas.DataFrame]
            The input coordinate dataframe.
        kde_bandwidth : float
            Bandwidth for kernel density estimation.
        minimum_expression : int
            Minimum expression value for local maxima determination.
        min_pixel_distance : int
            Minimum pixel distance for local maxima determination.
        coord_columns : Iterable[str], optional
            Name of the coordinate columns in the coordinate dataframe.
        gene_column : str, optional
            Name of the gene column in the coordinate dataframe.
        n_workers : int, optional
            Number of parallel workers for sampling.
        mode : str, optional
            Sampling mode, either '2d' or '3d'.
        patch_length : int
            Size of the length in each dimension when calculating signal integrity in patches.
            Smaller values will use less memory, but may take longer to compute.
        dtype
            Datatype for the KDE.

    Returns
    -------
        pandas.DataFrame: Gene expression KDE of local maxima.
        numpy.ndarray: Coordinates of local maxima
    """

    coord_columns = list(coord_columns)

    if mode is None:
        mode = f"{len(coord_columns)}d"

    if mode == "2d":
        print("Analyzing in 2d mode")
        coord_columns = coord_columns[:2]
    elif mode == "3d":
        print("Analyzing in 3d mode")
    else:
        raise ValueError(
            "Could not determine whether to use '2d' or '3d' analysis mode. Please specify mode='2d' or mode='3d'."
        )

    coordinates = coordinates[coord_columns + [gene_column]].copy()

    # lower resolution instead of increasing bandwidth!
    coordinates[coord_columns] /= kde_bandwidth

    print("determining pseudocells")

    # perform a global KDE to determine local maxima:
    vector_field_norm = _utils._kde_nd(
        coordinates[coord_columns].values, bandwidth=1, dtype=dtype
    )
    local_maximum_coordinates = _utils.find_local_maxima(
        vector_field_norm,
        min_pixel_distance=1 + int(min_pixel_distance / kde_bandwidth),
        min_expression=minimum_expression,
    )

    print("found", len(local_maximum_coordinates), "pseudocells")

    size = vector_field_norm.shape
    del vector_field_norm

    # truncate * bandwidth=1 -> _TRUNCATE * 1
    padding = _TRUNCATE

    print("sampling expression:")
    patches = []
    coords = []
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        for patch_df, offset, patch_size in tqdm.tqdm(
            _patches(coordinates, patch_length, padding, size=size),
            total=n_patches(patch_length, size),
        ):
            patch_maxima = local_maximum_coordinates[
                (local_maximum_coordinates[:, 0] >= offset[0])
                & (local_maximum_coordinates[:, 0] < offset[0] + patch_size[0])
                & (local_maximum_coordinates[:, 1] >= offset[1])
                & (local_maximum_coordinates[:, 1] < offset[1] + patch_size[1]),
                :,
            ]
            coords.append(patch_maxima)

            # we need to shift the maximum coordinates so they are in the correct
            # relative position of the patch
            maxima = patch_maxima.copy()
            maxima[:, 0] -= offset[0]
            maxima[:, 1] -= offset[1]

            # patch_size is 2D, make 3D if KDE is calculated as 3D
            patch_size = (
                patch_size[0] + 2 * padding,
                patch_size[1] + 2 * padding,
                *size[2:],
            )
            futures = {}
            for gene, df in patch_df.groupby(gene_column, observed=True):
                future = executor.submit(
                    _utils.kde_and_sample,
                    df[coord_columns].to_numpy(),
                    maxima,
                    size=patch_size,
                    bandwidth=1,
                    dtype=dtype,
                )
                futures[future] = gene

            patches.append(
                pd.DataFrame({futures[f]: f.result() for f in as_completed(futures)})
            )
            del futures

    gene_list = sorted(coordinates[gene_column].unique())
    coords = np.vstack(coords) * kde_bandwidth
    expression = pd.concat(patches).reset_index(drop=True)[gene_list].fillna(0)

    return expression, coords
