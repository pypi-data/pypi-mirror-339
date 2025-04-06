import magpack.io
import ThreeDViewer.data
from importlib import resources
from ThreeDViewer import plot_3d, plot_quiver
from ThreeDViewer.vector import plot_vector_field


def example():
    """Plots an example magnetization structure using three different functions.

    See :ref:`example` for a more detailed description.
    """
    data_path_resource = resources.files(ThreeDViewer.data) / 'cylinder.ovf'
    with data_path_resource as resource:
        data = magpack.io.load_ovf(resource)
    vf = data.magnetization
    plot_vector_field(vf)
    plot_3d(vf, arrow_skip=1, init_take=2)
    plot_quiver(vf[..., :, 15, :], slice_axis=1, skip=4, arrow_color=(0.5, 0.5, 0.5, 1))


if __name__ == "__main__":
    example()
