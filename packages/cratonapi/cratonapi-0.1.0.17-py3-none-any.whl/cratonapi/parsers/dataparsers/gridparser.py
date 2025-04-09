import struct

import numpy as np

from cratonapi.datacontainers import Grid


def parse(message: bytes) -> Grid:
    if len(message) < 16:
        raise RuntimeError("Incomplete message!")
    signature = message[0:4].decode("utf-8")
    if signature != "WSPM":
        raise RuntimeError("Incorrect signature!")
    size, operation, request, uid = struct.unpack("<IHHI", message[4:16])
    if operation != 3 or request != 7:
        raise RuntimeError("Incorrect operation or request codes!")
    if len(message) - 8 != size:
        raise RuntimeError("Incomplete message!")
    if uid == 0:
        raise RuntimeError("Desmana is not open!")

    grid_identifier = struct.unpack("<I", message[16:20])[0]
    n_x, n_y, x_min, x_max, y_min, y_max, z_min, z_max, blank_code = struct.unpack(
        "<2H7d", message[20:80]
    )
    data = struct.unpack(f"<{n_x * n_y}d", message[80 : 80 + (8 * n_x * n_y)])
    return Grid(
        grid_identifier,
        n_x,
        n_y,
        x_min,
        x_max,
        y_min,
        y_max,
        z_min,
        z_max,
        blank_code,
        np.asarray(data),
    )
