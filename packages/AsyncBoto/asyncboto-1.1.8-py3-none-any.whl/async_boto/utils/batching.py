from typing import Any


def chunks(list_: list[Any], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list_), n):
        yield list_[i : i + n]


def list_to_batches(list_: list[Any], batch_size: int) -> list[list[Any]]:
    return list(chunks(list_, batch_size))
