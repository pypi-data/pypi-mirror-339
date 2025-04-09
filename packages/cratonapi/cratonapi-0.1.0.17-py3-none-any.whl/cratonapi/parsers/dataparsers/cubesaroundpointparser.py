import struct
from typing import Tuple, List


def parse(message: bytes) -> Tuple[int, List[int]]:
    if len(message) < 16:
        raise RuntimeError("Incomplete message!")
    signature = message[0:4].decode("utf-8")
    if signature != "WSPM":
        raise RuntimeError("Incorrect signature!")
    size, operation, request, uid = struct.unpack("<IHHI", message[4:16])
    if operation != 3 or request != 21:
        raise RuntimeError("Incorrect operation or request codes!")
    if len(message) - 8 != size:
        raise RuntimeError("Incomplete message!")
    if uid == 0:
        raise RuntimeError("Desmana is not open!")

    number_of_cubes = struct.unpack("<H", message[16:18])[0]
    start = 18
    end = 22
    cube_ids = []
    for i in range(number_of_cubes):
        cube_ids.append(struct.unpack("<I", message[start:end])[0])
        start += 4
        end += 4
    return (number_of_cubes, cube_ids)
