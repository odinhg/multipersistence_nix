import multipers as mp
from pathlib import Path
import numpy as np
import shutil
import subprocess
import time

from utils import get_scc_filtration_size, get_kcritical_simplextree_size, compute_rhomboid_tiling, uniform_unit_square

def benchmark(X: np.ndarray, k_max: int, k_step: int=1) -> dict:
    results = {}

    # Delaunay core bifiltration
    print(f"Computing Delaunay core...", end="")
    t_start = time.time()
    st = mp.filtrations.CoreDelaunay(X, ks=range(1, k_max + 1, k_step))
    t_end = time.time()
    core_delaunay_time = t_end - t_start
    print(f" done ({core_delaunay_time:.2f} s). Now computing size...")
    core_delaunay_size = get_kcritical_simplextree_size(st)
    results["core_delaunay_time"] = core_delaunay_time
    results["core_delaunay_size"] = core_delaunay_size
    print(f"Computed Delaunay core in {core_delaunay_time:.2f} seconds with size {core_delaunay_size}.")

    return results

if __name__ == "__main__":
    seed = 0
    # Benchmarks to run (n, k_max, k_step, d) where we sample n points from [0,1]^d 
    param_grid = [
            (10_000, 100, 1, 2),
            (20_000, 100, 1, 2),
            (30_000, 100, 1, 2),
            (40_000, 100, 1, 2),
            (10_000, 1000, 10, 2),
            (20_000, 1000, 10, 2),
            (30_000, 1000, 10, 2),
            (40_000, 1000, 10, 2),
            (10_000, 100, 1, 3),
            (20_000, 100, 1, 3),
            (30_000, 100, 1, 3),
            (40_000, 100, 1, 3),
            (10_000, 1000, 10, 3),
            (20_000, 1000, 10, 3),
            (30_000, 1000, 10, 3),
            (40_000, 1000, 10, 3),
            ]

    output_dir = Path("./results")
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / "delaunay_core_benchmark_results.txt"

    rng = np.random.default_rng(seed)
    all_results = {}

    n_experiments = len(param_grid) 
    current_experiment = 1
    
    for n, k_max, k_step, d in param_grid:
        print(f"{current_experiment}/{n_experiments}: n={n}, k_max={k_max}, k_step={k_step}, d={d}")
        points = uniform_unit_square(n, rng, d=d)
        results = benchmark(points, k_max, k_step=k_step)
        all_results[(n, k_max, k_step, d)] = results
        current_experiment += 1

    print("Final results:")
    for (n, k_max, k_step, d), results in all_results.items():
        print(f"n={n}, k_max={k_max}, k_step={k_step}, d={d}")
        for key, value in results.items():
            if isinstance(value, float):
                print(f" {key}: {value:.2f}")
            else:
                print(f" {key}: {value}")

    # Save results to file in a LaTeX-friendly format
    with open(results_file, "w") as f:
        f.write("n & d & k_max & k_step & core_delaunay_size & core_delaunay_time \\\\\n")
        for (n, k_max, k_step, d), results in all_results.items():
            row = ""
            row += f"{n:,} & {d} & {k_max} & {k_step} & "
            # Format size with commas on thousands
            row += f"{results['core_delaunay_size']:,} & "
            # Time with 2 decimal places
            row += f"{results['core_delaunay_time']:.2f} \\\\\n"
            f.write(row)

    print(f"Results saved to {results_file}.")
