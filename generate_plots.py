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

def plot_signed_measure(slicer_or_st, homology_dimension: int, k_max: int, plot_title: str, filename: str, show_colorbar: bool = True, show_y_axis: bool = True):
    print(f"Computing signed measure and plotting...")
    signed_measure, = mp.signed_measure(slicer_or_st, degree=homology_dimension, invariant="hilbert")
    _ = mp.point_measure.integrate_measure(*signed_measure, plot=True)

    ax = plt.gca()
    ax.set_title(f"{plot_title}")
    ax.set_xlabel("r")
    ax.set_ylabel("k")
    ax.set_ylim(-k_max, 0)
    ax.set_xlim(0, 1.2)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune="both"))
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune=None))

    if not show_colorbar:
        fig = plt.gca().figure
        cbar_ax = fig.axes[1]
        fig.delaxes(cbar_ax)
        fig.subplots_adjust()

    if not show_y_axis:
        ax.set_yticks([])
        ax.set_ylabel("")

    for axis in plt.gcf().get_axes():
        axis.tick_params(axis='x', pad=12)
        axis.tick_params(axis='y', pad=12)

    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()
    print(f"Plot saved to {filename}")

def plot_pointcloud(X: np.ndarray, filename: str):
    plt.scatter(*X.T, s=10, color="black")
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.title("")
    plt.xlabel("x")
    plt.ylabel("y")
    for axis in plt.gcf().get_axes():
        axis.tick_params(axis='x', pad=12)
        axis.tick_params(axis='y', pad=12)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()
    print(f"Point cloud plot saved to {filename}")

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    point_clouds = [uniform_circle(100, 0, rng), uniform_circle(70, 30, rng), uniform_circle(30, 70, rng)]

    output_dir = Path("./plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    k_max = 100
    homology_dimension = 1
    beta = 1.0

    for i, X in enumerate(point_clouds):
        print(f"Processing point cloud {i+1}/{len(point_clouds)}...")
        # Plot the point cloud
        plot_pointcloud(X, output_dir / f"point_cloud_{i}.eps") 

        # Rhomboid tiling bifiltration (unsliced)
        print("Computing rhomboid tiling bifiltration (unsliced)...")
        slicer = rhomboid_tiling_slicer(X, k_max=k_max, homology_dimension=homology_dimension, sliced=False)
        plot_signed_measure(slicer, homology_dimension, k_max, "Rhomboid", output_dir / f"unsliced_rhomboid_tiling_signed_measure_{i}.eps", show_y_axis=True, show_colorbar=True)

        # Delaunay Core bifiltration
        print("Computing Delaunay Core bifiltration...")
        st = mp.filtrations.CoreDelaunay(X, beta=beta, ks=np.arange(1, k_max + 1, 1))
        plot_signed_measure(st, homology_dimension, k_max, "Delaunay Core", output_dir / f"delaunay_core_signed_measure_{i}.eps", show_y_axis=True, show_colorbar=True)
