# The Rhomboid Tiling Bifiltration in 2025

This repo contains scripts to build `rhomboidtiling` from source using an older versions of `CGAL`.

## How to use it

First, have `nix` installed and simply run `nix-shell --pure`. This will drop you into a shell with all required dependencies.

### Building required software

#### Building `rhomboidtiling`

Run `sh ./build_rhomboidtiling.sh` to build. To use, run the binary `./rhomboidtiling`.

#### Building `mpfree`

Run `sh ./build_mpfree.sh` to build. To use, run the binary `./mpfree`.

## Observations

### Choosing the dimension

There is a argument that does not seem to be documented in `rhomboidtiling`. Namely, if one is outputting FIRep files, there is an extra argument specifying the dimension $p$. The output file will contain the simplices of dimension $p$ and $p+1$. For example, if we are interested in $H_p$, we should run

```python
./rhomboid <point cloud file> <output firep file> 2 <k_max> firep <p>
```

for a point cloud in $\mathbb{R}^2$ with $k$ ranging from $0$ to `<k_max>`.

---

Tested on `EndeavourOS Linux x86_64 (6.16.1-arch1-1)`.

## Some Background

[1] Corbet, René, et al. "Computing the multicover bifiltration." Discrete & Computational Geometry 70.2 (2023): 376-405. 

[2] Edelsbrunner, Herbert, and Georg Osang. "The multi-cover persistence of Euclidean balls." Discrete & Computational Geometry 65.4 (2021): 1296-1313.

[3] Edelsbrunner, Herbert, and Georg Osang. "A simple algorithm for higher-order Delaunay mosaics and alpha shapes." Algorithmica 85.1 (2023): 277-295.
