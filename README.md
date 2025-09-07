# The rhomboid tiling and the Delaunay core bifiltration

This repo contains scripts to run benchmarks and Hilbert function plots for the rhomboid tiling and the Delaunay core bifiltrations, and also everything needed to build `rhomboidtiling` from source using an older versions of `CGAL`.

## How to use it

First, have `nix` installed and simply run `nix-shell --pure`. This will drop you into a shell with all required dependencies.

### Building required software

#### Building `rhomboidtiling`

Run `sh ./build_rhomboidtiling.sh` to build. The binary is added to your path, so you can run `rhomboidtiling` from anywhere in your nix-shell. 

#### Building `mpfree`

Run `sh ./build_mpfree.sh` to build. The binary is added to your path, so you can run `mpfree` from anywhere in your nix-shell.

### Running experiments

#### Running benchmarks (comparing with the rhomboid tiling bifiltration)

Run `uv run run_benchmarks.py` to run becnhmarks on point clouds uniformly sampled from the unit square. Results are saved to `results/benchmark_results.txt` by default in a LaTeX friendly format.

Dependencies are handled by `uv` so no additional setup is required.

#### Generating Hilbert function plots

Run `uv run generate_plots.py` to compute and plot the Hilbert function for the (unsliced) rhomboid tiling and the core Delaunay bifiltrations. By default, three point clouds sampled from $S^1$ with varying amounts of outliers will be used. Plots are saved in `plots/`.

#### Size benchmarks for the Delaunay core bifiltration

Run `uv run benchmark_delaunay_core.py` to run benchmarks on larger point clouds (only for the Delaunay core bifiltration). The results are saved to `results/delaunay_core_benchmark_results.txt` by default.

## Related papers 

[1] Corbet, René, et al. "Computing the multicover bifiltration." Discrete & Computational Geometry 70.2 (2023): 376-405. 

[2] Edelsbrunner, Herbert, and Georg Osang. "The multi-cover persistence of Euclidean balls." Discrete & Computational Geometry 65.4 (2021): 1296-1313.

[3] Edelsbrunner, Herbert, and Georg Osang. "A simple algorithm for higher-order Delaunay mosaics and alpha shapes." Algorithmica 85.1 (2023): 277-295.

[4] Blaser, Nello, et al. "Core bifiltration." arXiv preprint arXiv:2405.01214 (2024).
