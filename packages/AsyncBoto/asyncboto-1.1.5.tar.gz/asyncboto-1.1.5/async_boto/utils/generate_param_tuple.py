from typing import Any


def generate_param_tuple(params: dict[str, Any]) -> list[tuple]:
    """
    To support MultiValueQueryParameters these cant be given using a dict.
    We convert these dict to a list of key value pairs and let aiohttp and
    botocore handle the rest.

    """
    new_params = []
    for key, value in params.items():
        if isinstance(value, list):
            for value_ in value:
                new_params.append((key, value_))
        elif isinstance(value, bool):
            new_params.append((key, str(value)))
        else:
            new_params.append((key, value))
    return sorted(new_params)
