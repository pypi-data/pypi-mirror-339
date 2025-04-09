"""Module for parsing and writing DCMI structured value strings
"""

import json
import re
from collections.abc import Mapping
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
    return {_decode_value(key): _decode_value(value) for key, value in data.items()}


def dumps(data: Any | Mapping = None, **kwargs) -> str:
    """Write value or mapping as structured value string"""
    if data is None:
        data = {}
    elif not isinstance(data, Mapping):
        return _encode_value(data)
    data.update(**kwargs)
    return "; ".join(
        f"{_encode_value(key)}={_encode_value(value)}" for key, value in data.items()
    )
