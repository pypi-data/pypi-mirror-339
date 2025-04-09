from importlib.metadata import version
from re import match, sub

from glue.core import BaseData
from glue.viewers.common.state import LayerState


PLOTLY_MAJOR_VERSION = int(version("plotly").split(".")[0])


__all__ = [
    'cleaned_labels',
    'mpl_ticks_values',
    'opacity_value_string',
    'rgba_string_to_values',
    'is_rgba_hex',
    'is_rgb_hex',
    'rgba_hex_to_rgb_hex',
]


def cleaned_labels(labels):
    cleaned = [sub(r'\\math(default|regular)', r'\\mathrm', label) for label in labels]
    for j in range(len(cleaned)):
        label = cleaned[j]
        if '$' in label:
            cleaned[j] = '${0}$'.format(label.replace('$', ''))
    return cleaned


def mpl_ticks_values(axes, axis):
    index = 1 if axis == 'y' else 0
    minor_getters = [axes.get_xminorticklabels, axes.get_yminorticklabels]
    minor_ticks = minor_getters[index]()
    if not (minor_ticks and any(t.get_text() for t in minor_ticks)):
        return [], []
    major_getters = [axes.get_xticklabels, axes.get_yticklabels]
    major_ticks = major_getters[index]()
    vals, text = [], []
    for tick in major_ticks + minor_ticks:
        txt = tick.get_text()
        if txt:
            vals.append(tick.get_position()[index])
            text.append(txt)
        text = cleaned_labels(text)
    return vals, text


def opacity_value_string(a):
    asint = int(a)
    asfloat = float(a)
    n = asint if asint == asfloat else asfloat
    return str(n)


DECIMAL_PATTERN = "\\d+\\.?\\d*"
RGBA_PATTERN = f"rgba\\(({DECIMAL_PATTERN}),\\s*({DECIMAL_PATTERN}),\\s*({DECIMAL_PATTERN}),\\s*({DECIMAL_PATTERN})\\)"


def rgba_string_to_values(rgba_str):
    m = match(RGBA_PATTERN, rgba_str)
    if not m or len(m.groups()) != 4:
        raise ValueError("Invalid RGBA expression")
    r, g, b, a = m.groups()
    return [int(t) for t in (r, g, b, a)]


def is_rgba_hex(color):
    return color.startswith("#") and len(color) == 9


def is_rgb_hex(color):
    return color.startswith("#") and len(color) == 7


def rgba_hex_to_rgb_hex(color):
    return color[:-2]


def hex_string(number):
    return format(number, '02x')


def rgb_hex_to_rgba_hex(color, opacity=1):
    return f"{color}{hex_string(opacity)}"


def hex_to_components(color):
    return [int(color[idx:idx+2], 16) for idx in range(1, len(color), 2)]


def rgba_components(color):
    if is_rgb_hex(color):
        color = rgb_hex_to_rgba_hex(color)
    if is_rgba_hex(color):
        return hex_to_components(color)
    else:
        return rgba_string_to_values(color)


def components_to_hex(r, g, b, a=None):
    components = [hex_string(t) for t in (r, g, b, a) if t is not None]
    return f"#{''.join(components)}"


def data_for_layer(layer_or_state):
    if isinstance(layer_or_state.layer, BaseData):
        return layer_or_state.layer
    else:
        return layer_or_state.layer.data


def frb_for_layer(viewer_state,
                  layer_or_state,
                  bounds):

    data = data_for_layer(layer_or_state)
    layer_state = layer_or_state if isinstance(layer_or_state, LayerState) else layer_or_state.state
    is_data_layer = data is layer_or_state.layer
    target_data = getattr(viewer_state, 'reference_data', data)
    data_frb = data.compute_fixed_resolution_buffer(
        target_data=target_data,
        bounds=bounds,
        target_cid=layer_state.attribute
    )

    if is_data_layer:
        return data_frb
    else:
        subcube = data.compute_fixed_resolution_buffer(
            target_data=target_data,
            bounds=bounds,
            subset_state=layer_state.layer.subset_state
        )
        return subcube * data_frb


def font(family, size, color) -> dict:
    return dict(
        family=family,
        size=size,
        color=color
    )


def add_title(config, text, font=None):
    if PLOTLY_MAJOR_VERSION == 6:
        title = dict(text=text)
        if font:
            title["font"] = font
        config.update(title=title)
    else:
        config["title"] = text
        if font:
            config["titlefont"] = font
