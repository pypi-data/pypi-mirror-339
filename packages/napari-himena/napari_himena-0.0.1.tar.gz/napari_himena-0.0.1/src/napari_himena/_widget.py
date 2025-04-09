from __future__ import annotations

from collections.abc import Callable

import napari
import numpy as np
from cmap import Colormap
from himena import StandardType, new_window
from himena.profile import profile_dir
from himena.standards import roi
from himena.standards.model_meta import ArrayAxis, ImageChannel, ImageMeta
from napari.layers import (
    Image,
    Labels,
    Layer,
    Points,
    Shapes,
    Surface,
)
from qtpy import QtCore
from qtpy import QtWidgets as QtW


class QNapariHimenaPipeline(QtW.QWidget):
    def __init__(self, napari_viewer: napari.Viewer):
        super().__init__()
        self._napari_viewer = napari_viewer
        self._layout = QtW.QVBoxLayout(self)
        self._specify_profile = QSpecifyProfileWidget()
        self._specify_profile.connected.connect(self._connect_himena)
        self._layout.addWidget(self._specify_profile)
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def _connect_himena(self, profile_name: str):
        self._himena_ui = new_window(
            profile_name, plugins=["napari_himena.himena_commands"]
        )
        # register type "napari.Viewer" to make it available in himena
        self._himena_ui.model_app.injection_store.register_provider(
            self._provide_napari_viewer,
            weight=10,
        )

        # Create buttons for each action
        self._layout.addWidget(
            _make_btn("Image to Himena", self._image_to_himena)
        )
        self._layout.addWidget(
            _make_btn("Labels to Himena", self._labels_to_himena)
        )
        self._layout.addWidget(
            _make_btn("Points to Himena", self._points_to_himena)
        )
        self._layout.addWidget(
            _make_btn("Shapes to Himena", self._shapes_to_himena)
        )
        self._layout.addWidget(
            _make_btn("Feature to Himena", self._feature_to_himena)
        )
        self._layout.addWidget(QtW.QWidget(), stretch=100)  # Spacer
        self._specify_profile.setEnabled(False)
        self._himena_ui.show()

    def _provide_napari_viewer(self) -> napari.Viewer:
        """Provide the napari viewer to himena."""
        return self._napari_viewer

    def _image_to_himena(self):
        if isinstance(layer := self._current_layer(), Image):
            arr = layer.data
            layer_cmap = layer.colormap.name
            try:
                _cmap = Colormap(layer_cmap)
            except ValueError:
                _cmap = Colormap("gray")
            self._himena_ui.add_object(
                arr,
                type=StandardType.IMAGE,
                title=layer.name,
                metadata=ImageMeta(
                    axes=[
                        ArrayAxis(
                            name=layer.axis_labels[i], scale=layer.scale[i]
                        )
                        for i in range(arr.ndim)
                    ],
                    channels=[
                        ImageChannel(
                            colormap=_cmap.name,
                            contrast_limits=layer.contrast_limits,
                        )
                    ],
                    is_rgb=layer.rgb,
                ),
            )

    def _labels_to_himena(self):
        if isinstance(layer := self._current_layer(), Labels):
            arr = layer.data
            axis_labels = layer.axis_labels
            self._himena_ui.add_object(
                arr,
                type=StandardType.IMAGE_LABELS,
                title=layer.name,
                metadata=ImageMeta(
                    axes=[
                        ArrayAxis(name=axis_labels[i], scale=layer.scale[i])
                        for i in range(arr.ndim)
                    ],
                ),
            )

    def _shapes_to_himena(self):
        if isinstance(layer := self._current_layer(), Shapes):
            items = []
            indices = []
            for data, stype in zip(layer.data, layer.shape_type, strict=True):
                if stype == "rectangle":
                    height, width = np.max(
                        np.abs(np.diff(data[:, -2:], axis=0)), axis=0
                    )
                    y0, x0 = np.min(data[:, -2:], axis=0)
                    _roi = roi.RectangleRoi(
                        x=x0, y=y0, width=width, height=height
                    )
                elif stype == "ellipse":
                    height, width = np.max(
                        np.abs(np.diff(data[:, -2:], axis=0)), axis=0
                    )
                    y0, x0 = np.min(data[:, -2:], axis=0)
                    _roi = roi.EllipseRoi(
                        x=x0, y=y0, width=width, height=height
                    )
                elif stype == "line":
                    start = data[0, -2:]
                    end = data[1, -2:]
                    _roi = roi.LineRoi(
                        start=tuple(start[::-1]), end=tuple(end[::-1])
                    )
                elif stype == "path":
                    ys = data[:, -2]
                    xs = data[:, -1]
                    _roi = roi.SegmentedLineRoi(ys=ys, xs=xs)
                elif stype == "polygon":
                    ys = data[:, -2]
                    xs = data[:, -1]
                    _roi = roi.PolygonRoi(ys=ys, xs=xs)
                else:
                    raise ValueError(f"Unknown shape type: {stype}")
                if data.shape[1] > 2:
                    multi = np.unique(data[:, :-2], axis=0)
                    if multi.shape[0] == 1:
                        indices.append(multi[0])
                    else:
                        raise ValueError("Shapes must be in 2D slices")
                else:
                    indices.append(np.zeros((1, 0), dtype=int))
                items.append(_roi)
            roi_list = roi.RoiListModel(
                items=items,
                indices=np.stack(indices, axis=0),
                axis_names=layer.axis_labels,
            )
            self._himena_ui.add_object(
                roi_list, type=StandardType.ROIS, title=layer.name
            )
        else:
            raise TypeError(
                f"Layer type {layer.__class__.__name__} is not supported for shapes."
            )

    def _feature_to_himena(self):
        if isinstance(
            layer := self._current_layer(), (Labels, Points, Shapes, Surface)
        ):
            df = layer.features
            self._himena_ui.add_object(
                df,
                type=StandardType.DATAFRAME,
                title=f"Features of {layer.name}",
            )
        else:
            raise TypeError(
                f"Layer type {layer.__class__.__name__} is not supported for features."
            )

    def _points_to_himena(self):
        if isinstance(layer := self._current_layer(), Points):
            arr = layer.data
            columns = layer.axis_labels
            point_data = {
                col: arr[:, i].copy() for i, col in enumerate(columns)
            }
            self._himena_ui.add_object(
                point_data,
                type=StandardType.DATAFRAME,
                title=layer.name,
            )
        else:
            raise TypeError(
                f"Layer type {layer.__class__.__name__} is not supported for points."
            )

    def _current_layer(self) -> Layer | None:
        """Get the current layer in the viewer."""
        return self._napari_viewer.layers.selection.active


def _make_btn(text: str, callback: Callable[[], None]) -> QtW.QPushButton:
    """Create a button with the given text and callback."""
    btn = QtW.QPushButton(text)
    btn.clicked.connect(callback)
    btn.setToolTip(callback.__doc__)
    return btn


class QSpecifyProfileWidget(QtW.QWidget):
    """Widget to specify a profile for the napari viewer."""

    connected = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._choices = QtW.QComboBox(self)
        self._choices.addItems(
            [
                profile_file.stem
                for profile_file in profile_dir().glob("*.json")
            ]
        )
        self._connect_btn = QtW.QPushButton("Connect")
        self._connect_btn.clicked.connect(
            lambda: self.connected.emit(self._choices.currentText())
        )
        self.setToolTip("Select which himena profile to use.")
        layout = QtW.QHBoxLayout(self)
        layout.addWidget(self._choices)
        layout.addWidget(self._connect_btn)
        layout.setContentsMargins(0, 0, 0, 0)
