# The Rhomboid Tiling Bifiltration in 2025

This repo contains scripts to build `rhomboidtiling` from source using an older versions of `CGAL`.

## How to use it

First, have `nix` installed and simply run `nix-shell --pure`. This will drop you into a shell with all required dependencies.

### Building required software

#### Building `rhomboidtiling`

Run `sh ./build_rhomboidtiling.sh` to build. To use, run the binary `./rhomboidtiling`.

#### Building `mpfree`

Run `sh ./build_mpfree.sh` to build. To use, run the binary `./mpfree`.

### Running experiments

#### Running benchmarks

Run `uv run run_benchmarks.py` to run becnhmarks on point clouds uniformly sampled from the unit square. Results are saved to `results/benchmark_results.txt` by default in a LaTeX friendly format.


## Related papers 

[1] Corbet, René, et al. "Computing the multicover bifiltration." Discrete & Computational Geometry 70.2 (2023): 376-405. 

[2] Edelsbrunner, Herbert, and Georg Osang. "The multi-cover persistence of Euclidean balls." Discrete & Computational Geometry 65.4 (2021): 1296-1313.

[3] Edelsbrunner, Herbert, and Georg Osang. "A simple algorithm for higher-order Delaunay mosaics and alpha shapes." Algorithmica 85.1 (2023): 277-295.

[4] Blaser, Nello, et al. "Core bifiltration." arXiv preprint arXiv:2405.01214 (2024).
