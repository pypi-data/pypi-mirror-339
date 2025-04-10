from datetime import timedelta
from mpvis.mpdfg.utils.color_scales import (
    TIME_COLOR_SCALE,
    FREQUENCY_COLOR_SCALE,
    COST_COLOR_SCALE,
)


def dimensions_min_and_max(activities, connections):
    activities_dimensions = next(iter(activities.values())).keys()
    connections_dimensions = next(iter(connections.values())).keys()
    dimensions_min_and_max = {key: (0, 0) for key in activities_dimensions}

    for dim in activities_dimensions:
        min_val = min((activity[dim] for activity in activities.values()))
        max_val = max((activity[dim] for activity in activities.values()))
        dimensions_min_and_max[dim] = (min_val, max_val)

    for dim in connections_dimensions:
        min_val = min((connection[dim] for connection in connections.values()))
        max_val = max((connection[dim] for connection in connections.values()))
        prev_min_val = dimensions_min_and_max[dim][0]
        prev_max_val = dimensions_min_and_max[dim][1]
        dimensions_min_and_max[dim] = (min(prev_min_val, min_val), max(prev_max_val, max_val))

    return dimensions_min_and_max


def ids_mapping(activities):
    id = 0
    mapping = {}
    for activity in activities.keys():
        mapping[activity] = f"A{id}"
        id += 1

    return mapping


def background_color(measure, dimension, dimension_scale):
    colors_palette_scale = (90, 255)
    color_palette = color_palette_by_dimension(dimension)
    assigned_color_index = round(interpolated_value(measure, dimension_scale, colors_palette_scale))
    return color_palette[assigned_color_index]


def color_palette_by_dimension(dimension):
    if dimension == "frequency":
        return FREQUENCY_COLOR_SCALE
    elif dimension == "cost":
        return COST_COLOR_SCALE
    else:
        return TIME_COLOR_SCALE


def interpolated_value(measure, from_scale, to_scale):
    measure = max(min(measure, from_scale[1]), from_scale[0])
    denominator = max(1, (from_scale[1] - from_scale[0]))
    normalized_value = (measure - from_scale[0]) / denominator
    interpolated_value = to_scale[0] + normalized_value * (to_scale[1] - to_scale[0])
    return interpolated_value


def format_time(total_seconds):
    delta = timedelta(seconds=total_seconds)
    years = round(delta.days // 365)
    months = round((delta.days % 365) // 30)
    days = round((delta.days % 365) % 30)
    hours = round(delta.seconds // 3600)
    minutes = round((delta.seconds % 3600) // 60)
    seconds = round(delta.seconds % 60)

    if years > 0:
        return "{:02d}y {:02d}m {:02d}d ".format(years, months, days)
    if months > 0:
        return "{:02d}m {:02d}d {:02d}h ".format(months, days, hours)
    if days > 0:
        return "{:02d}d {:02d}h {:02d}m ".format(days, hours, minutes)
    if hours > 0:
        return "{:02d}h {:02d}m {:02d}s ".format(hours, minutes, seconds)
    if minutes > 0:
        return "{:02d}m {:02d}s".format(minutes, seconds)
    if seconds > 0:
        return "{:02d}s".format(seconds)
    return "Instant"


def link_width(measure, dimension_scale):
    width_scale = (1, 8)
    link_width = round(interpolated_value(measure, dimension_scale, width_scale), 2)
    return link_width
