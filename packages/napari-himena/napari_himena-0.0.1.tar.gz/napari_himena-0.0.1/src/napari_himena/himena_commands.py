import napari
import numpy as np
from cmap import Colormap
from himena import Parametric, StandardType, WidgetDataModel
from himena._app_model import HimenaApplication
from himena.data_wrappers import wrap_dataframe
from himena.plugins import configure_gui, configure_submenu, register_function
from himena.standards import roi
from himena.standards.model_meta import ImageMeta

_SEND = ["tools/send-to-napari", "/model_menu/send-to-napari"]
configure_submenu(_SEND, title="Send to napari ...")


def _get_or_create_viewer() -> "napari.Viewer":
    if viewer := napari.current_viewer():
        return viewer
    return napari.Viewer()


def _install_provider():
    try:
        app = next(iter(HimenaApplication._instances.values()))
    except StopIteration:
        app = HimenaApplication.get_or_create("test")
    app.injection_store.register_provider(_get_or_create_viewer)


_install_provider()


@register_function(
    menus=_SEND,
    title="As Points",
    types=[StandardType.TABLE, StandardType.DATAFRAME, StandardType.ARRAY],
)
def send_table_as_points(
    model: WidgetDataModel, viewer: "napari.Viewer"
) -> None:
    if model.is_subtype_of(StandardType.DATAFRAME):
        df = wrap_dataframe(model.value)
        axis_labels = df.column_names()
        arr = np.stack([df[col] for col in axis_labels], axis=1)
    else:
        arr = np.asarray(model.value, dtype=np.float32)
        axis_labels = None
    viewer.add_points(arr, name=model.title, axis_labels=None)


@register_function(
    menus=_SEND,
    title="As Features",
    types=[StandardType.TABLE, StandardType.DATAFRAME],
)
def send_table_as_features(
    model: WidgetDataModel, viewer: "napari.Viewer"
) -> Parametric:
    layer_choices = [
        (ly.name, ly) for ly in viewer.layers if hasattr(ly, "features")
    ]

    @configure_gui(layer={"choices": layer_choices})
    def send_features(layer) -> None:
        layer.features = model.value

    return send_features


@register_function(
    menus=_SEND,
    title="As Image",
    types=StandardType.IMAGE,
)
def send_image_as_image(
    model: WidgetDataModel, viewer: "napari.Viewer"
) -> None:
    """Send image from a himena subwindow to the napari viewer."""
    arr = model.value
    kwargs = {"name": model.title}
    if isinstance(meta := model.metadata, ImageMeta):
        kwargs["channel_axis"] = meta.channel_axis
        if meta.channel_axis is not None:
            kwargs["colormap"] = [
                Colormap(chn.colormap).to_napari() for chn in meta.channels
            ]
            kwargs["contrast_limits"] = [
                chn.contrast_limits for chn in meta.channels
            ]
            kwargs["axis_labels"] = [
                axis.name
                for i, axis in enumerate(meta.axes)
                if i != meta.channel_axis
            ]
        else:
            kwargs["colormap"] = Colormap(
                meta.channels[0].colormap
            ).to_napari()
            kwargs["contrast_limits"] = meta.channels[0].contrast_limits
            kwargs["axis_labels"] = [axis.name for axis in meta.axes]
        kwargs["rgb"] = meta.is_rgb
    viewer.add_image(arr, **kwargs)


@register_function(
    menus=_SEND,
    title="ROIs As Points",
    types=[StandardType.IMAGE, StandardType.ROIS],
)
def send_rois_as_points(
    model: WidgetDataModel, viewer: "napari.Viewer"
) -> None:
    rois = _get_rois(model)
    data = []
    for multi, each_roi in rois.iter_with_indices():
        if isinstance(each_roi, roi.PointRoi2D):
            data.append(
                np.array([multi + (each_roi.y, each_roi.x)])[np.newaxis]
            )
        elif isinstance(each_roi, roi.PointsRoi2D):
            multi_array = np.repeat(
                np.expand_dims(multi, axis=0), len(each_roi.xs), axis=0
            )
            data.append(
                np.stack([multi_array, each_roi.ys, each_roi.xs], axis=1)
            )
        else:
            raise ValueError(
                f"Cannot convert ROI type {type(each_roi)} to points"
            )
    data = np.concatenate(data, axis=0)
    viewer.add_points(data, name=model.title, size=5)


@register_function(
    menus=_SEND,
    title="ROIs As Shapes",
    types=[StandardType.IMAGE, StandardType.ROIS],
)
def send_rois_as_shapes(
    model: WidgetDataModel, viewer: "napari.Viewer"
) -> None:
    rois = _get_rois(model)
    shape_types = []
    data = []
    inv_xy = (slice(None), slice(None, None, -1))
    for multi, each_roi in rois.iter_with_indices():
        if isinstance(each_roi, roi.LineRoi):
            shape_types.append("line")
            shape = np.stack([each_roi.start, each_roi.end], axis=0)[inv_xy]
        elif isinstance(each_roi, roi.PolygonRoi):
            shape_types.append("polygon")
            shape = np.stack([each_roi.ys, each_roi.xs], axis=1)[inv_xy]
        elif isinstance(each_roi, roi.SegmentedLineRoi):
            shape_types.append("path")
            shape = np.stack([each_roi.ys, each_roi.xs], axis=1)[inv_xy]
        elif isinstance(each_roi, roi.RectangleRoi):
            shape_types.append("rectangle")
            shape = np.stack(
                [
                    (each_roi.y, each_roi.x),
                    (each_roi.y, each_roi.x + each_roi.width),
                    (
                        each_roi.y + each_roi.height,
                        each_roi.x + each_roi.width,
                    ),
                    (each_roi.y + each_roi.height, each_roi.x),
                ],
                axis=0,
            )
        elif isinstance(each_roi, roi.EllipseRoi):
            shape_types.append("ellipse")
            shape = np.stack(
                [
                    (each_roi.y, each_roi.x),
                    (each_roi.y, each_roi.x + each_roi.width),
                    (
                        each_roi.y + each_roi.height,
                        each_roi.x + each_roi.width,
                    ),
                    (each_roi.y + each_roi.height, each_roi.x),
                ],
                axis=0,
            )
        else:
            raise ValueError(f"Unknown ROI type: {type(each_roi)}")
        if len(multi) == 0:
            data.append(shape)
        else:
            multi_array = np.repeat(
                np.expand_dims(multi, axis=0), shape.shape[0], axis=0
            )
            data.append(np.stack([multi_array, shape], axis=1))
    viewer.add_shapes(data, shape_type=shape_types, name=model.title)


def _get_rois(model: WidgetDataModel) -> roi.RoiListModel:
    if model.is_subtype_of(StandardType.IMAGE):
        if not isinstance(meta := model.metadata, ImageMeta):
            raise ValueError("ROIs are not available in the image metadata")
        rois = meta.unwrap_rois()
    elif model.is_subtype_of(StandardType.ROIS):
        if not isinstance(rois := model.value, roi.RoiListModel):
            raise ValueError("ROIs are not available in the image metadata")
    else:
        raise ValueError("ROIs are not available in this model type.")
    return rois
