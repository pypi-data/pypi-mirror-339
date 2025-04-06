import logging
import magpack.vectorop
from magpack.image_utils import hls2rgb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def axial_align(orientation_field, index):
    """Aligns the components of an orientation field such that a singular direction (index) is always positive.

    Parameters
    ----------
    orientation_field : np.ndarray
        The orientation field to align.
    index : {'x', 'y', 'z'}
        The axis to align towards, {'x', 'y' or 'z'}.

    Returns
    -------
    np.ndarray
        Aligned components of orientation field along specified axis.
    """
    x, y, z = np.array(orientation_field)  # make a copy such that the input data are not changed
    mask = locals()[index] < 0 if index in ('x', 'y', 'z') else None

    if mask is not None:
        x[mask], y[mask], z[mask] = -x[mask], -y[mask], -z[mask]
    else:
        raise ValueError('Index not recognised.')
    return np.array([x, y, z])


def plot_3d(data, fig=None, init_take=1, init_slice=0, axial=False,
            save=None, const_color=False, arrow_skip=0, show=True, axes_names=None, title='',
            mode=4, **kwargs):
    """Plots a 3D scalar or vector field, with the possibility to slice along different axes.

    Plotting maintains a right-handed axis system, looking down from the slicing axis.

    Parameters
    ----------
    data : np.ndarray
        The 3D scalar or vector field to plot.
    fig : :class:`matplotlib.figure.Figure` (optional)
        Matplotlib figure to use (by default a new figure will be created).
    init_take : int (optional)
        Initial slicing direction (0, 1, 2) corresponding to the (x, y, z) spatial dimensions.
    init_slice : int (optional)
        Initial slice index.
    axial : bool (optional)
        True for orientation field coloring, False for vector field coloring.
    save : str (optional)
        Filename to save a snapshot of the figure.
    const_color : bool (optional)
        Vector coloring will remain the same regardless of the slicing axis when True.
    arrow_skip : int (optional)
        Add arrows to the plot, 0 implies no arrows.
    show : bool (optional)
        True to show figure, false will maintain the figure for plotting later with plt.show().
    axes_names : 3-tuple of string (optional)
        Axis names to use for plotting.
    title : str (optional)
        Title of the figure.
    mode : int | callable (optional)
        Lightness mapping mode (1 - 4) or function (see :func:`vector_color`).

    Returns
    -------
    Slider, Slider (optional)
        Slice and axis slider objects, necessary to maintain interactivity when `show` is set to `False`.

    Other Parameters
    ----------------
    kwargs : matplotlib.artist.Artist properties
        Additional keyword arguments for matplotlib (e.g. cmap).
    """
    multi_color = None
    vf = np.array(data)
    # check if the input is a vector field
    if data.ndim == 4 and data.shape[-1] != 3 and data.shape[0] == 3:
        if const_color:
            # create rgb image, new shape will be (initial shape, 3)
            data = vector_color(data, axial=axial, oop=init_take, mode=mode)
        else:
            # get a different color for each slicing option such that black and white are out-of- and into-plane colors
            # new shape will be (3, initial shape, 3)
            multi_color = np.stack([vector_color(data, axial=axial, oop=ii, mode=mode) for ii in range(3)])
            data = multi_color[init_take]
    elif data.ndim == 3:
        # make sure arrows are set to false since there is no vector field
        arrow_skip = 0

    elif data.ndim != 3:
        raise ValueError("Data not 3D and cannot be plotted.")

    if fig is None:
        fig = plt.figure()
    fig.suptitle(title)

    if axes_names is None:
        axes_names = ('x', 'y', 'z')

    # globals
    take_axis = [init_take]  # slicing axis
    slice_index = [init_slice]  # slicing index, starts at 0
    extents = _get_extents(data)  # array of extents

    # image plot space
    ax = fig.add_axes((0.25, 0.25, 0.7, 0.7), anchor='SW')
    _set_axis_labels(ax, take_axis[0], axes_names)

    first_img = np.take(data, slice_index[0], axis=take_axis[0])
    # for the y-axis, an axis swap is not necessary since the data are already in (z, x) form
    if take_axis[0] != 1:
        first_img = first_img.swapaxes(0, 1)
    image = ax.imshow(first_img, origin='lower', extent=extents[take_axis[0]], **kwargs)

    if arrow_skip < 0:
        arrow_skip = 0

    if arrow_skip:
        h_axis, v_axis = _get_components(take_axis[0])
        handle = [_add_quiver(ax, np.take(vf, slice_index[0], take_axis[0] + 1)[[h_axis, v_axis]], axial,
                              arrow_skip, take_axis[0] == 1)]

    if data.ndim == 3:
        if "vmin" in kwargs and isinstance(kwargs["vmin"], (int, float)):
            vmin = kwargs["vmin"]
        else:
            vmin = np.nanmin(data)
        if "vmax" in kwargs and isinstance(kwargs["vmax"], (int, float)):
            vmax = kwargs["vmax"]
        else:
            vmax = np.nanmax(data)

        fig.colorbar(image, ax=ax)
        image.set_clim((vmin, vmax))

    # adjust the main plot to make room for the sliders
    ax_slice = fig.add_axes((0.3, 0.075, 0.5, 0.025))
    slice_slider = Slider(ax=ax_slice, label='slice', valmin=0, valmax=data.shape[take_axis[0]] - 1, valstep=1,
                          valinit=init_slice)

    ax_axis_slice = fig.add_axes((0.075, 0.25, 0.025, 0.5))
    ax_slice_slider = Slider(ax=ax_axis_slice, label='slice axis', valmin=0, valmax=2, valinit=init_take, valstep=1,
                             orientation="vertical")

    def draw():
        if multi_color is not None:
            img = np.take(multi_color[int(take_axis[0])], int(slice_index[0]), axis=take_axis[0])
        else:
            img = np.take(data, int(slice_index[0]), axis=take_axis[0])

        if take_axis[0] != 1:
            img = img.swapaxes(0, 1)

        if arrow_skip:
            h, v = _get_components(take_axis[0])
            handle[0].remove()
            handle[0] = _add_quiver(ax, np.take(vf, slice_index[0], take_axis[0] + 1)[[h, v]], axial,
                                    arrow_skip, take_axis[0] == 1)
            image.set_extent(extents[take_axis[0]])  # quiver takes over the axes extent thus need to enforce

        image.set_data(img)
        fig.canvas.draw_idle()

    def slice_update(val):
        slice_index[0] = val
        if data.shape[take_axis[0]] < slice_index[0]:
            slice_index[0] = 0
        slice_slider.valmax = data.shape[take_axis[0]] - 1  # doesn't work visually but keeps the slider in the limits
        draw()

    def slice_axis_update(val):
        take_axis[0] = val
        slice_slider.valmax = data.shape[take_axis[0]] - 1  # doesn't work visually but avoids errors
        slice_slider.ax.set_xlim(slice_slider.valmin, slice_slider.valmax)

        if data.shape[take_axis[0]] < slice_index[0]:
            slice_index[0] = data.shape[take_axis[0]] - 1
            slice_slider.set_val(slice_index[0])

        image.set_extent(extents[take_axis[0]])
        _set_axis_labels(ax, take_axis[0], axes_names)
        draw()

    # register the update function with each slider
    slice_slider.on_changed(slice_update)
    ax_slice_slider.on_changed(slice_axis_update)

    if save:
        fig.savefig(save)
        plt.close(fig)
        return None

    if show:
        plt.show()

    return slice_slider, ax_slice_slider


def vector_color(data, saturation=1, mode=4, axial=False, oop=1):
    r"""Converts a 3D or 2D array of 3 components into a complex number, which can then be plotted using complex domain
    coloring.

    The input should be an array with [x, y, z] vector components. Each component can have 2 or 3 spatial dimensions
    thus the input array should have the shape (3, nx, ny).

    The mapping of the out of plane component can be done linearly or with some other function to improve contrast.
    The available modes are:

    1. Linear:          :math:`l = y`
    2. Root:            :math:`l = \pm\sqrt{y}`
    3. Tangential:      :math:`l = \frac {2}{\pi} \tan{y}`
    4. Cubic:           :math:`l = y^3`

    Parameters
    ----------
    data : np.ndarray
        Input vector field numpy array shaped (3, x, y) or (3, x, y, z).
    saturation : float (optional)
        0...1 for color saturation or 0 to colour according to magnitude.
    mode : int (optional) | callable
        Choice (0 - 4) for lightness maps described above or mapping function.
    axial : bool (optional)
        Apply degenerate coloring for orientation fields.
    oop : int (optional)
        Index of out-of-plane direction.

    Returns
    -------
    np.ndarray
        RBG array (x, y, z, 3) for plotting.
    """
    if oop not in (0, 1, 2):
        raise ValueError("Out-of-plane parameter must be an integer from 0 to 2.")

    # apply axial alignment if
    axial_axes = {0: 'x', 1: 'y', 2: 'z'}
    if axial:
        data = axial_align(data, axial_axes[oop])

    # even permutations for other out-of-plane choices
    permute = {0: (2, 0, 1), 1: (0, 1, 2), 2: (1, 2, 0)}
    data = data[permute[oop], ...]
    x, y, z = data

    hue = np.arctan2(x, z)


    y_norm = y / np.max(magpack.vectorop.magnitude(data))

    lightness_map = {1 : lambda x : x,
                     2 : lambda x : np.sign(x) * np.sqrt(np.abs(x)),
                     3 : lambda x : 2 * np.tan(x) / np.pi,
                     4 : lambda x : x ** 3}

    if isinstance(mode, int):
        mode = lightness_map.get(mode)
    if callable(mode):
        y_norm = mode(y_norm)
    else:
        logging.warning("Lightness mapping defaulting to linear.")

    if axial:
        # axial is applied if the field is mostly in-plane and degenerate coloring is necessary
        if np.count_nonzero(np.sqrt(x ** 2 + z ** 2) > np.abs(y)):
            hue *= 2

    lightness = (y_norm + 1) / 2
    mag = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    lightness = np.where(mag == 0, 1, lightness)  # make the background white
    if not 0 <= saturation <= 1:
        saturation = 1
    elif saturation == 0:
        saturation = mag / np.max(mag)
    return hls2rgb(hue, lightness, saturation)


def plot_quiver(data, slice_axis=2, axial=False, skip=4, save=None, saturation=1, show=True, arrow_color=None,
                title='', mode=4):
    """Plots vectors using complex color and adds a quiver overlay for clarity.

    Parameters
    ----------
    data : np.ndarray
        Vector or orientation array with shape (3, nx, ny).
    slice_axis : int (optional)
        Index from which the slice was taken (so that out-of-plane component can be determined).
    axial : bool (optional)
        True for orientations, False for vector fields.
    skip : int (optional)
        Number of arrows to skip for visual clarity.
    save : str (optional)
        Filename to which the figure will be saved.
    saturation : float (optional)
        Color saturation, None for magnitude-based
    show : bool (optional)
        True to show figure, false will maintain the figure for plotting later with plt.show().
    arrow_color : 4-tuple (optional)
        Arrow colors in RGBA values from 0 to 1.
    title : str (optional)
        Title of the figure.
    mode : int (optional) | callable
        Choice (0 - 4) for lightness map or callable mapping function (see :func:`vector_color`).
    """

    sizes = data.shape
    components, spatial_dims = sizes[0], sizes[1:]

    if not (components in [2, 3]):
        raise ValueError("Quiver plot vector field must have 2 or 3 components.")
    if len(spatial_dims) != 2:
        raise ValueError("Quiver plot vector field must have 2 spatial dimensions.")
    if components == 2:
        data = np.concatenate([data, np.zeros((1,) + spatial_dims)], axis=0)

    # get color
    color = vector_color(data, axial=axial, oop=slice_axis, saturation=saturation, mode=mode)
    if slice_axis != 1:
        color = color.transpose((1, 0, 2))

    h_axis, v_axis = _get_components(slice_axis)

    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_axes((0.2, 0.2, 0.7, 0.7), anchor='SW')
    extent = (0., color.shape[1], 0., color.shape[0])
    ax.imshow(color, origin='lower', extent=extent)

    _add_quiver(ax, data[[h_axis, v_axis]], axial, skip, permute=slice_axis == 1, arrow_color=arrow_color)
    _set_axis_labels(ax, slice_axis)

    if save:
        fig.savefig(save)
        plt.close(fig)
        return None

    if show:
        plt.show()


def _add_quiver(axes, data, axial, skip, permute, arrow_color=None):
    """Adds quivers to the current axis.

    Parameters
    ----------
    axes : matplotlib.axes.Axes
        The :class:`Axes` on which to add quivers.
    data : np.ndarray
        Vector or orientation array with shape (2, nx, ny).
    axial : bool (optional)
        True for orientations, False for vector fields.
    skip : int (optional)
        Number of arrows to skip for visual clarity.
    permute : bool (optional)
        For axes of odd permutation, the horizontal and vertical axes should be swapped.
    arrow_color : 4-tuple (optional)
        The color of the arrows.
    """
    sx, sy = data.shape[-2:]
    xx, yy = np.meshgrid(np.linspace(0.5, sx - 0.5, sx),
                         np.linspace(0.5, sy - 0.5, sy), indexing='ij')
    xx, yy = (yy, xx) if permute else (xx, yy)

    # create an array that skips every nth (n=skip) arrow, similar to [::skip]
    skips = (slice(None, None, skip), slice(None, None, skip))
    arrow_x, arrow_y = data[0][skips], data[1][skips]
    if arrow_color is None:
        arrow_color = (0, 0, 0, 1)  # defaults to black arrows
    if axial:
        arrow_kwarg = dict(headwidth=1, headaxislength=0, headlength=0)
    else:
        arrow_kwarg = {}
    return axes.quiver(xx[skips], yy[skips], arrow_x, arrow_y, pivot='mid', scale=1 / skip, units='xy',
                       scale_units='xy', angles='xy', minlength=0, **arrow_kwarg, color=arrow_color)


def _get_components(take_axis):
    # get x and y coordinates by removing 0, 1 or 2 from the array (0, 1, 2)
    x_idx, y_idx = np.delete(np.arange(3), take_axis)
    # removing the middle axis makes an odd permutation, swap axes to maintain right-handedness
    if take_axis == 1:
        x_idx, y_idx = y_idx, x_idx
    return x_idx, y_idx


def _get_extents(data):
    r"""Gets extents of vector field data.

    In order to maintain a right-handed coordinate system, looking down the slicing axis, the extent choices are:

    - slicing along x (axis = 0) implies y (horizontal axis) and z (vertical axis) are plotted.
    - slicing along y (axis = 1) implies z (horizontal axis) and x (vertical axis) are plotted.
    - slicing along z (axis = 2) implies x (horizontal axis) and y (vertical axis) are plotted.


    Parameters
    ----------
    data : np.ndarray
        Array for creating a list of extents for plotting.

    Returns
    -------
    3-list of 4-tuples
        List of tuples containing extents for each of the slicing options.
    """
    extents = [(0, data.shape[1], 0, data.shape[2]),
               (0, data.shape[2], 0, data.shape[0]),
               (0, data.shape[0], 0, data.shape[1])]
    return extents


def _set_axis_labels(ax, take_axis, axes_names=None):
    """Set axes labels for the plots, given the plot axes and slicing axis.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes object from the figure.
    take_axis : int {0, 1, 2}
        Index of axis that is being sliced (0, 1, 2).
    axes_names : 3-tuple of str
        Names of the axes, default is x, y and z.
    """
    if axes_names is None:
        axes_names = ('x', 'y', 'z')

    if take_axis == 0:
        ax.set_xlabel(axes_names[1])
        ax.set_ylabel(axes_names[2])
    elif take_axis == 1:
        ax.set_xlabel(axes_names[2])
        ax.set_ylabel(axes_names[0])
    elif take_axis == 2:
        ax.set_xlabel(axes_names[0])
        ax.set_ylabel(axes_names[1])
