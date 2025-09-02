import multipers as mp
from multipers.simplex_tree_multi import SimplexTreeMulti_type
from multipers.slicer import Slicer_type
from pathlib import Path
import numpy as np
import shutil
import subprocess
import time

def get_scc_filtration_size(file_path: str | Path) -> int:
    # Count simplices, subtract firep header lines
    with open(file_path, "r") as f:
        num_lines = sum(1 for _ in f) - 4
    return num_lines

def get_kcritical_simplextree_size(st: SimplexTreeMulti_type) -> int:
    # Since Delaunay core is multi-critical, we count all critical filtration values (not only simplices)
    return sum(len(x[1]) for x in st.get_simplices())

def compute_rhomboid_tiling(point_cloud_file: str | Path, output_file: str | Path, dim: int, k_max: int, homology_dimension: int, sliced: bool=True) -> float:
    """Compute the rhomboid tiling bifiltration using the external rhomboidtiling binary."""
    method = "firep" if sliced else "ufirep"
    t_start = time.time()
    subprocess.run(["rhomboidtiling", str(point_cloud_file), str(output_file), str(dim), str(k_max), method, str(homology_dimension)], capture_output=True, text=True)
    t_end = time.time()
    t_delta = t_end - t_start
    return t_delta

def rhomboid_tiling_slicer(X: np.ndarray, k_max: int, homology_dimension: int, sliced: bool=True) -> Slicer_type:
    """Point cloud to multipers Slicer for the rhomboid tiling bifiltration (sliced and unsliced). Multipers runs mpfree on the filtration."""
    temp_folder = Path("./temp_rhomboid_tiling_slicer")
    temp_folder.mkdir(parents=True, exist_ok=True)
    input_file = temp_folder / "points.txt"
    output_file = temp_folder / "rhomboid_out"
    
    np.savetxt(input_file, X, fmt="%.18f")
    
    t_delta = compute_rhomboid_tiling(input_file, output_file, X.shape[1], k_max, homology_dimension, sliced=sliced)
    print(f"Rhomboid tiling computed in {t_delta:.2f} seconds.")
    
    t_start = time.time()
    slicer = mp.Slicer()
    mp.io.scc_reduce_from_str_to_slicer(output_file, slicer, backend="mpfree", dimension=homology_dimension, verbose=False)
    t_end = time.time()
    print(f"Slicer object created and reduced in {t_end - t_start:.2f} seconds.")

    # Clean up temp folder
    shutil.rmtree(temp_folder)
    return slicer

def uniform_unit_square(n: int, rng: np.random.Generator) -> np.ndarray:
    """Generate n uniformly distributed points in a unit square."""
    return np.random.rand(n, 2)
