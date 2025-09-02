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

def benchmark(X: np.ndarray, k_max: int, delete_temp: bool=True) -> dict:
    results = {}

    # Delaunay core bifiltration
    print(f"Computing Delaunay core...")
    t_start = time.time()
    st = mp.filtrations.CoreDelaunay(X, ks=range(1, k_max + 1))
    t_end = time.time()
    core_delaunay_time = t_end - t_start
    core_delaunay_size = get_kcritical_simplextree_size(st)
    results["core_delaunay_time"] = core_delaunay_time
    results["core_delaunay_size"] = core_delaunay_size
    print(f"Computed Delaunay core in {core_delaunay_time:.2f} seconds with size {core_delaunay_size}.")

    # Rhomboid tiling bifiltrations
    homology_dimension = 1
    temp_folder = Path("./temp_rhomboid_tiling")
    temp_folder.mkdir(parents=True, exist_ok=True)
    input_file = temp_folder / "points.txt"
    output_file_sliced = temp_folder / "rhomboid_out_sliced"
    output_file_unsliced = temp_folder / "rhomboid_out_unsliced"
    np.savetxt(input_file, X, fmt="%.18f")

    print("Computing Sliced Rhomboid tiling...")
    sliced_rhomboid_time = compute_rhomboid_tiling(input_file, output_file_sliced, X.shape[1], k_max, homology_dimension, sliced=True)
    sliced_rhomboid_size = get_scc_filtration_size(output_file_sliced)
    results["sliced_rhomboid_time"] = sliced_rhomboid_time
    results["sliced_rhomboid_size"] = sliced_rhomboid_size
    print(f"Computed sliced rhomboid tiling in {sliced_rhomboid_time:.2f} seconds with size {sliced_rhomboid_size}.")

    print("Computing Unsliced Rhomboid tiling...")
    unsliced_rhomboid_time = compute_rhomboid_tiling(input_file, output_file_unsliced, X.shape[1], k_max, homology_dimension, sliced=False)
    unsliced_rhomboid_size = get_scc_filtration_size(output_file_unsliced)
    results["unsliced_rhomboid_time"] = unsliced_rhomboid_time
    results["unsliced_rhomboid_size"] = unsliced_rhomboid_size
    print(f"Computed unsliced rhomboid tiling in {unsliced_rhomboid_time:.2f} seconds with size {unsliced_rhomboid_size}.")

    # Clean up temp folder
    if delete_temp:
        print(f"Cleaning up {temp_folder}...")
        shutil.rmtree(temp_folder)

    return results


def uniform_unit_square(n: int, rng: np.random.Generator) -> np.ndarray:
    """Generate n uniformly distributed points in a unit square."""
    return np.random.rand(n, 2)


if __name__ == "__main__":
    seed = 0
    sizes = [10_000, 20_000, 30_000, 40_000] # Skipped 80k due to hardware limitations
    #sizes = [100, 200, 300, 400]  # Smaller sizes for testing and debugging
    ks_max = [4, 8]

    output_dir = Path("./results")
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / "benchmark_results.txt"

    rng = np.random.default_rng(seed)
    all_results = {}

    n_experiments = len(sizes) * len(ks_max)
    current_experiment = 1
    point_clouds = [uniform_unit_square(n, rng) for n in sizes]
    for k_max in ks_max:
        for i, n in enumerate(sizes):
            print(f"{current_experiment}/{n_experiments}: n={n}, k_max={k_max}")
            points = point_clouds[i]
            results = benchmark(points, k_max, delete_temp=True)
            all_results[(n, k_max)] = results
            current_experiment += 1

    print("Final results:")
    for (n, k_max), results in all_results.items():
        print(f"n={n}, k_max={k_max}")
        for key, value in results.items():
            if isinstance(value, float):
                print(f" {key}: {value:.2f}")
            else:
                print(f" {key}: {value}")

    # Save results to file in a LaTeX-friendly format
    with open(results_file, "w") as f:
        f.write("n & k_max & core_delaunay_size & core_delaunay_time & sliced_rhomboid_size & sliced_rhomboid_time & unsliced_rhomboid_size & unsliced_rhomboid_time \\\\\n")
        for (n, k_max), results in all_results.items():
            f.write(f"{n} & {k_max} & {results['core_delaunay_size']} & {results['core_delaunay_time']:.2f} & {results['sliced_rhomboid_size']} & {results['sliced_rhomboid_time']:.2f} & {results['unsliced_rhomboid_size']} & {results['unsliced_rhomboid_time']:.2f} \\\\\n")

    print(f"Results saved to {results_file}.")

