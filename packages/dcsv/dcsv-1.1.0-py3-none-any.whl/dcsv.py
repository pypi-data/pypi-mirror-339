"""Module for parsing and writing DCMI structured value strings"""

import json
import re
from collections.abc import Iterable, Mapping
from typing import Any


def _encode_value(value: Any) -> str:
    """Encode a value as string escaping special characters"""
    if isinstance(value, str):
        return value.replace(";", "\\;").replace("=", "\\=")
    else:
        return json.dumps(value, default=str)


def _replace_escaped_special_chars(text: str) -> str:
    """Replace escaped special characters with placeholders"""
    return str(text).replace("\\;", "SEMICOLON").replace("\\=", "EQUALS SIGN")


def _decode_value(text: str) -> str:
    """Decode a value from a string replacing special characters into placeholders"""
    text = text.replace("SEMICOLON", ";").replace("EQUALS SIGN", "=")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def loads(text: str) -> dict:
    """Parse a structured value string to a dictionary"""
    data = dict(
        re.findall(
            r"([^;]+?)=([^;]+);?\s?",
            # Replace special characters with placeholders
            _replace_escaped_special_chars(text),
        )
    )
    if not data:
        return _decode_value(text)
    decoded = {_decode_value(key): _decode_value(value) for key, value in data.items()}
    if all(re.match(r"#(\d+)", str(key)) for key in decoded.keys()):
        output = []
        for i_key, value in decoded.items():
            i, key = re.match(r"#(\d+)\.(.*)", i_key).groups()
            i = int(i)
            try:
                output[i].update({key: value})
            except IndexError:
                output.insert(i, {key: value})
    else:
        output = decoded
    return output


def dumps(data: Any | Mapping = None, upper_key: str | None = None, **kwargs) -> str:
    """Write value or mapping as structured value string

    Args:
        data: Data to be written (optional)
        upper_key: Upper level key (optional)
        kwargs: Keyword arguments are added to the data
    """
    if data is None:
        data = {}
    elif isinstance(data, Iterable) and all(isinstance(item, Mapping) for item in data):
        data = {
            f"#{i}.{key}": value
            for i, item_data in enumerate(data, start=1)
            for key, value in item_data.items()
        }
    elif not isinstance(data, Mapping):
        return _encode_value(data)
    data.update(**kwargs)
    output = []
    for key, value in data.items():
        if isinstance(value, Mapping):
            output.append(dumps(value, upper_key=key))
        else:
            if upper_key:
                key = f"{upper_key}.{key}"
            output.append(f"{_encode_value(key)}={_encode_value(value)}")
    return "; ".join(output)
