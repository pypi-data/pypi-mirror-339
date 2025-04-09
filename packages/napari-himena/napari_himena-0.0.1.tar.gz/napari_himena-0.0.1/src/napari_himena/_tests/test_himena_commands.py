from collections.abc import Callable

import napari
import numpy as np
from himena import StandardType, create_model
from himena.standards.model_meta import ArrayAxis, ImageChannel, ImageMeta
from numpy.testing import assert_equal

from napari_himena import himena_commands as hcmd


def test_send_table(make_napari_viewer: Callable[[], napari.Viewer]):
    viewer = make_napari_viewer()
    hcmd.send_table_as_points(
        create_model(
            np.array([[1, 2], [3, 4], [5, 6]]),
            type=StandardType.TABLE,
        ),
        viewer,
    )
    assert len(viewer.layers) == 1
    assert_equal(viewer.layers[0].data, np.array([[1, 2], [3, 4], [5, 6]]))

    viewer.layers.clear()
    hcmd.send_table_as_points(
        create_model(
            np.array([[3, 1, 2], [3, 3, 4], [2, 5, 6]]),
            type=StandardType.TABLE,
        ),
        viewer,
    )
    assert len(viewer.layers) == 1
    assert_equal(viewer.layers[0].data, [[3, 1, 2], [3, 3, 4], [2, 5, 6]])

    viewer.layers.clear()
    hcmd.send_table_as_points(
        create_model(
            {"y": np.array([1, 2, 3]), "x": np.array([4, 5, 6])},
            type=StandardType.DATAFRAME_PLOT,
        ),
        viewer,
    )
    assert len(viewer.layers) == 1
    assert_equal(viewer.layers[0].data, [[1, 4], [2, 5], [3, 6]])


def test_sending_image(make_napari_viewer: Callable[[], napari.Viewer]):
    viewer = make_napari_viewer()
    img = np.arange(24).reshape(6, 4)
    hcmd.send_image_as_image(
        create_model(
            img,
            type=StandardType.IMAGE,
            metadata=ImageMeta(
                axes=[
                    ArrayAxis(name="y", scale=0.8),
                    ArrayAxis(name="x", scale=0.6),
                ],
            ),
        ),
        viewer,
    )
    assert_equal(viewer.layers[-1].data, img)
    viewer.layers.clear()
    img = np.arange(24).reshape(2, 3, 4)
    hcmd.send_image_as_image(
        create_model(
            img,
            type=StandardType.IMAGE,
            metadata=ImageMeta(
                axes=[
                    ArrayAxis(name="c"),
                    ArrayAxis(name="y", scale=0.8),
                    ArrayAxis(name="x", scale=0.6),
                ],
                channels=[
                    ImageChannel(colormap="green", contrast_limits=(0, 24)),
                    ImageChannel(colormap="magenta", contrast_limits=(0, 20)),
                ],
                channel_axis=0,
            ),
        ),
        viewer,
    )
    assert len(viewer.layers) == 2
    assert_equal(viewer.layers[0].data, img[0])
    assert_equal(viewer.layers[1].data, img[1])
    assert viewer.layers[0].colormap.name == "cmap_green"
    assert viewer.layers[1].colormap.name == "cmap_magenta"
    assert viewer.layers[0].contrast_limits == [0, 24]
    assert viewer.layers[1].contrast_limits == [0, 20]
