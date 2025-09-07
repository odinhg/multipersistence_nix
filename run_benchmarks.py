import multipers as mp
from pathlib import Path
import numpy as np
import shutil
import subprocess
import time

from utils import get_scc_filtration_size, get_kcritical_simplextree_size, compute_rhomboid_tiling, uniform_unit_square

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
    output_file_unsliced = temp_folder / "rhomboid_out_unsliced"
    np.savetxt(input_file, X, fmt="%.18f")

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

if __name__ == "__main__":
    seed = 0
    sizes = [10_000, 20_000, 40_000, 80_000] # Skipped 80k due to hardware limitations
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
        f.write("n & k_max & core_delaunay_size & unsliced_rhomboid_size & core_delaunay_time & unsliced_rhomboid_time \\\\\n")
        for (n, k_max), results in all_results.items():
            row = ""
            row += f"{n} & {k_max} & "
            # Format size with commas on thousands
            row += f"{results['core_delaunay_size']:,} & {results['unsliced_rhomboid_size']:,} & "
            # Time with 2 decimal places
            row += f"{results['core_delaunay_time']:.2f} & {results['unsliced_rhomboid_time']:.2f} \\\\\n"
            f.write(row)


    print(f"Results saved to {results_file}.")

