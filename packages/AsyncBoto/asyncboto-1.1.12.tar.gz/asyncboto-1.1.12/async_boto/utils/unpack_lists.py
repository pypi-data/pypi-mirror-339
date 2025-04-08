from typing import Any


def unpack_lists(list_: list[Any]) -> list[Any]:
    unpacked_list = []
    for item in list_:
        if isinstance(item, list):
            unpacked_list.extend(unpack_lists(item))
            continue
        unpacked_list.append(item)
    return unpacked_list
