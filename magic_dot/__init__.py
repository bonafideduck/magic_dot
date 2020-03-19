"""Top-level package for Magic Dot."""

__author__ = """Mark Eklund"""
__email__ = "magic_dot@patnan.com"
__version__ = "0.1.1"

__all__ = ["MagicDot", "NOT_FOUND"]

from typing import Optional, Any
from .exceptions import NotFound


class _NotFound:
    def __bool__(self):
        raise RuntimeError("NOT_FOUND does not support truthy operations.")

    def __repr__(self):
        return "magic_dot.NOT_FOUND"


NOT_FOUND = _NotFound()
"""The default return value when an item is not found."""


class MagicDot:
    """A wrapper that allows data extraction without all the `try` and `except` overhead."""

    def __init__(self, data: Any, lists: bool = True, exception: bool = False):
        """Main data wrapper for the MagicDot module

        Args:
           data: The data to be wrapped by MagicDot
           lists: Selects if expanded list support is enabled (see MagicDot.lists for more info.)
           exception: Selects if an exception is raised when get() would return magic_dot.NOT_FOUND

        Kwargs:
           bar (str): Really, same as foo.

        """
        self.__data = data
        self.__lists = lists
        self.__exception = exception

    def __create_child(
        self, data, lists: Optional[bool] = None, exception: Optional[bool] = None
    ):
        lists = self.__lists if lists is None else lists
        exception = self.__exception if exception is None else exception
        return MagicDot(data, lists=lists, exception=exception)

    def __bool__(self):
        raise RuntimeError(
            "MagicDot does not support truthy operations.  Extract data with .get() first."
        )

    def __getattr__(self, name):
        data = NOT_FOUND

        if hasattr(self.__data, name):
            data = getattr(self.__data, name)

        elif isinstance(self.__data, dict):
            data = self.__data.get(name, NOT_FOUND)

        elif data is NOT_FOUND and isinstance(self.__data, list) and self.__lists:
            data_list = []
            empties = 0
            for data in self.__data:
                if hasattr(data, name):
                    d = getattr(data, name)
                elif isinstance(data, dict):
                    d = data.get(name, NOT_FOUND)
                else:
                    d = NOT_FOUND
                if data_list:
                    data_list.append(d)
                elif d is not NOT_FOUND:
                    data_list = [NOT_FOUND] * empties + [d]
                else:
                    empties += 1

            if data_list:
                data = data_list
            else:
                data = NOT_FOUND

        return self.__create_child(data)

    def __getitem__(self, key):
        data = NOT_FOUND
        try:
            data = self.__data[key]
        except (AttributeError, KeyError, TypeError):
            if data is NOT_FOUND and isinstance(self.__data, list) and self.__lists:
                data_list = []
                empties = 0
                for data in self.__data:
                    try:
                        d = self.data[key]
                    except (AttributeError, KeyError, TypeError):
                        d = NOT_FOUND
                    if data_list:
                        data_list.append(d)
                    elif d is not NOT_FOUND:
                        data_list = [NOT_FOUND] * empties + [d]
                    else:
                        empties += 1

                if data_list:
                    data = data_list
                else:
                    data = NOT_FOUND

        return self.__create_child(data)

    def lists(self, lists: bool = True) -> "MagicDot":
        """Enable or disable expanded list support.

        When lists is enabled, if this has no key matches causing NOT_FOUND, 
        and the data is a list, the list contents will be searched for key matches
        If anything matches, a list containing extracted values will be created.  If 
        at least one, but not all list items have a match, the nonmatching items will
        be replaced with NOT_FOUND.

        Args:
            lists: Enable or disable spanning of lists.

        Returns:
            If the lists changes, a new MagicDot will be returned.  Otherwise,
            this returns self.
        """
        if self.__lists == lists:
            return self
        else:
            return self.__create_child(self.__data, lists=lists)

    def exception(self, exception: bool = True) -> "MagicDot":
        """Enable or disable exceptions when NOT_FOUND is encountered in a get().

        Args:
            exception: Enable or disable exceptions on a get().

        Returns:
            If the lists changes, a new MagicDot will be returned.  Otherwise,
            this returns self.
        """
        if self.__exception == exception:
            return self
        else:
            return self.__create_child(self.__data, exception=exception)

    def get(self, not_found: Any = NOT_FOUND, exception: bool = None):
        """Gets the data held within this MagicDot.

        Typically, this is either the data or NOT_FOUND.  If lists is enabled (the default)
        and the data is a list this will also replace any NOT_FOUND values within the first
        level of that list with `not_found`.

        Args:
           data: The data to be wrapped by MagicDot
           lists: Selects if expanded list support is enabled (see MagicDot.lists for more info.)
           exception: Selects if an exception is raised when this would return magic_dot.NOT_FOUND

        Returns:
            The data held withing this MagicDot instance.
        """
        exception = self.__exception if exception is None else exception

        if self.__data is NOT_FOUND:
            if exception and not_found is NOT_FOUND:
                raise NotFound
            return not_found
        elif isinstance(self.__data, list) and self.__lists:
            if not_found is not NOT_FOUND:
                return [d if d is not NOT_FOUND else not_found for d in self.__data]
            if exception and NOT_FOUND in self.__data:
                raise NotFound
        return self.__data
