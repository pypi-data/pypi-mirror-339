ThreeDViewer
============
ThreeDViewer is a plotting tool for visualizing 3D scalar and vector fields in python.

Installation
------------
ThreeDViewer can be installed through pip:

.. code-block::

   (.venv) $ pip install ThreeDViewer

Documentation
-------------
Comprehensive documentation is available online at
`readthedocs <https://ThreeDViewer.readthedocs.io/en/latest/index.html>`_.

Quickstart
----------
To view a 3D scalar, vector or orientation field and slice all axes interactively, use

.. code-block::

    ThreeDViewer.plot_3d(scalar_field)

For vector and orientation fields, each pixel will have a hue according to the vector's direction and a lightness
depending on the into-the-plane (bright) and out-of-plane (dark) components. This color adjusts according to the
viewing axis, but can be kept constant across different axes by setting the argument ``const_color`` to ``True``.

An example vector field is included in the package and the resulting plots are shown below

.. image:: doc/source/_static/images/middle.png
    :width: 300
    :alt: Middle slice along the z-axis of a magnetic cylinder with a vortex topology that points into the plane


.. image:: doc/source/_static/images/yslice.png
    :width: 300
    :alt: Middle slice along the y-axis of
