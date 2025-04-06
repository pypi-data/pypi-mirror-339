from collections.abc import Iterable
from typing import Any, Optional
import time

def string_is_number(string: str) -> bool:
    """
    Checks if string is a number or not.
    """
    if type(string) != str:
        raise TypeError(f"{type(string).__name__} {string} is not a string.")
    try:
        complex(string)
        return True
    except ValueError:
        return False

def format_key(string: str = None, uppercase: bool = False, replace_empty: str = None, delete_not_alpha: bool = False) -> str:
    """
    Formats a string.
    """
    formatted_string = None
    if string:
        if delete_not_alpha:
            for char in string:
                if not char.isalpha() and not char.isspace():
                    string = string.replace(char, '')

        if not uppercase:
            string = string.lower()
        else:
            string = string.upper()

        if replace_empty:
            string = string.replace(' ', replace_empty)

        formatted_string = string
    return formatted_string

def join_keys(keys: list[str] | tuple[str] = ['hello', 'world'], separator: str = '+') -> str:
    """
    Joins multiple string keys in a single string.
    """
    result = keys
    if isinstance(keys, Iterable) and type(keys) is not str:
        string_keys = (str(key) for key in keys)
        result = separator.join(string_keys)
    return str(result)

def generate_epoch_timestamp() -> int:
    timestamp: int = int(time.time())
    return timestamp

def get_index(object: tuple | list, index: int, default: Optional[Any] = None) -> Any | None:
    """
    Safely retrieves an element from a tuple or list by index.

    - **object** (tuple | list): The tuple or list from which to retrieve the element.
    - **index** (int): The index of the element to retrieve.
    - **default** (Any, optional): The value to return if the index is out of range. Defaults to None.

    **Returns**: The element at the specified index, or the default value if the index is out of range.
    """
    try:
        return object[index]
    except IndexError:
        return default

if __name__ == "__main__":
    ...