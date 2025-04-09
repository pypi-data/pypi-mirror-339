import struct

import numpy as np

from cratonapi.datacontainers import Color, GridDisplayProperties


def parse(message: bytes) -> GridDisplayProperties:
    if len(message) < 16:
        raise RuntimeError("Incomplete message!")
    signature = message[0:4].decode("utf-8")
    if signature != "WSPM":
        raise RuntimeError("Incorrect signature!")
    size, operation, request, uid = struct.unpack("<IHHI", message[4:16])
    if operation != 3 or request != 10:
        raise RuntimeError("Incorrect operation or request codes!")
    if len(message) - 8 != size:
        raise RuntimeError("Incomplete message!")
    if uid == 0:
        raise RuntimeError("Desmana is not open!")

    (
        isoline_min_level,
        isoline_max_level,
        isoline_level_step,
        minor_isoline_blue,
        minor_isoline_green,
        minor_isoline_red,
        minor_isoline_alpha,
        minor_isoline_thickness,
        major_isoline_blue,
        major_isoline_green,
        major_isoline_red,
        major_isoline_alpha,
        major_isoline_thickness,
        major_isoline_step,
        palette_min_level,
        palette_max_level,
        color_interpolation_type,
        points_count,
    ) = struct.unpack("<3f4Bf4BfH2dBI", message[16:67])
    offset: int = 0
    point_values = np.empty(points_count)
    point_colors = np.empty(points_count, Color)
    for point in range(points_count):
        value, blue, green, red, alpha = struct.unpack(
            "<f4B", message[67 + offset : 75 + offset]
        )
        offset += 8
        point_values[point] = value
        point_colors[point] = Color(alpha, red, green, blue)
    return GridDisplayProperties(
        isoline_min_level,
        isoline_max_level,
        isoline_level_step,
        Color(
            minor_isoline_alpha,
            minor_isoline_red,
            minor_isoline_green,
            minor_isoline_blue,
        ),
        minor_isoline_thickness,
        Color(
            major_isoline_alpha,
            major_isoline_red,
            major_isoline_green,
            major_isoline_blue,
        ),
        major_isoline_thickness,
        major_isoline_step,
        palette_min_level,
        palette_max_level,
        color_interpolation_type,
        point_values,
        point_colors,
    )
