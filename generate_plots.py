import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
import numpy as np
import multipers as mp
from pathlib import Path

from utils import rhomboid_tiling_slicer, uniform_circle

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 28}
matplotlib.rc('font', **font)
plt.rcParams["figure.figsize"] = (10, 10)

def plot_signed_measure(slicer_or_st, homology_dimension: int, k_max: int, plot_title: str, filename: str):
    print(f"Computing signed measure and plotting...")
    signed_measure, = mp.signed_measure(slicer, degree=homology_dimension, invariant="hilbert")
    _ = mp.point_measure.integrate_measure(*signed_measure, plot=True)

    ax = plt.gca()
    ax.set_title(f"{plot_title} H{homology_dimension}")
    ax.set_xlabel("r")
    ax.set_ylabel("k")
    ax.set_ylim(-k_max, 0)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune="both"))
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune=None))
    plt.savefig(filename)
    plt.clf()

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    X = uniform_circle(180, 20, rng)

    output_dir = Path("./plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    k_max = 100 
    homology_dimension = 1

    # Rhomboid tiling bifiltration (unsliced)
    slicer = rhomboid_tiling_slicer(X, k_max=k_max, homology_dimension=homology_dimension, sliced=False)
    plot_signed_measure(slicer, homology_dimension, k_max, "Rhomboid (unsliced)", output_dir / "unsliced_rhomboid_tiling_signed_measure.png")

    # Rhomboid tiling bifiltration (sliced)
    slicer = rhomboid_tiling_slicer(X, k_max=k_max, homology_dimension=homology_dimension, sliced=True)
    plot_signed_measure(slicer, homology_dimension, k_max, "Rhomboid (sliced)", output_dir / "sliced_rhomboid_tiling_signed_measure.png")

    # Delaunay Core bifiltration
    beta = 1
    st = mp.filtrations.CoreDelaunay(X, beta=beta, ks=range(1, k_max + 1))
    plot_signed_measure(st, homology_dimension, k_max, "Delaunay Core", output_dir / "delaunay_core_signed_measure.png")
