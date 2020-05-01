"""Top-level package for Magic Dot."""

__author__ = """Mark Eklund"""
__email__ = "magic_dot@patnan.com"
__version__ = "0.2.0"

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
    """A wrapper that allows data extraction without all the `try` and `except` overhead.

    Args:
        data: The data to be wrapped by MagicDot
        exception: Selects if a NotFound exception to be raised when NOT_FOUND happens during extraction.
        iter_nf_as_empty: Selects if iterating over NOT_FOUND should return an empty iterator.

    Note:
        The MagicDot class has no public attributes.  Any access to an attribute will be
        mapped to the underlying data and used to extract a new MagicDot structure.
    """

    def __init__(self, data: Any, exception: bool = False, iter_nf_as_empty: bool = False):
        self.__data = data
        self.__exception = exception
        self.__iter_nf_as_empty = iter_nf_as_empty

    def __create_child(
        self, data, exception: Optional[bool] = None, iter_nf_as_empty: Optional[bool] = None
    ):
        exception = self.__exception if exception is None else exception
        iter_nf_as_empty = self.__iter_nf_as_empty if iter_nf_as_empty is None else iter_nf_as_empty
        return MagicDot(data, exception=exception, iter_nf_as_empty=iter_nf_as_empty)

    def __bool__(self):
        raise RuntimeError(
            "MagicDot does not support truthy operations.  Extract data with .get() first."
        )

    def __getattr__(self, name):
        data = NOT_FOUND

        try:
            data = getattr(self.__data, name)
        except AttributeError:
            try:
                return self.__getitem__(name)
            except NotFound:
                raise NotFound from None
                    
        return self.__create_child(data)

    def __getitem__(self, key):
        try:
            data = self.__data[key]
        except (AttributeError, KeyError, TypeError):
            if self.__exception:
                raise NotFound from None
            else:
                data = NOT_FOUND

        return self.__create_child(data)
        
    def __iter__(self):
        """Contains iterator creatiion support for MagicDot.

        If an attempt is made to iterate over a MagicDot instance and the data
        is iterable, this supports walking those contents where the contents
        will also be wrapped in the MagicDot structure.

        If the data contained is NOT_FOUND, the current iter_nf_as_empty state 
        of the MagicDot instance is checked.  If not set, a TypeError will be
        raised.  If set, an empty iterator will be returned.

        Returns:
            The data held withing this MagicDot instance.
        """
        if self.__data is NOT_FOUND and self.__iter_nf_as_empty:
            return iter(())
        else:
            return (self.__create_child(x) for x in self.__data)


    def exception(self, exception: bool = True) -> "MagicDot":
        """Enable or disable exceptions when NOT_FOUND is encountered.

        NOT_FOUND is encountered whenever code extracts additional data
        from the encapsulated data.  Some examples would be: :::

          >>> from magic_dot import MagicDot
          >>> md = MagicDot([1])
          >>> md = md.exception()
          >>> md['nonexistent']
          (raises magic_dot.exceptions.NotFound)
          >>> md.nonexistent
          (raises magic_dot.exceptions.NotFound)
          >>> md.pluck('nonexistent')
          (raises magic_dot.exceptions.NotFound)
          
        Without exceptions enabled, the above would respectively return
        MagicDot(NOT_FOUND), MagicDot(NOT_FOUND) and MagicDot([NOT_FOUND]).

        Args:
            exception: Enable or disable exceptions when NOT_FOUND is encountered.

        Returns:
            If the exception changes, a new MagicDot will be returned.  Otherwise,
            this returns self.
        """
        if self.__exception == exception:
            return self
        else:
            return self.__create_child(self.__data, exception=exception)
 
    def iter_nf_as_empty(self, iter_nf_as_empty: bool = True) -> "MagicDot":
        """Enable or disable empty iterator support for NOT_FOUND data.

        By default, if a request is made to iterate over a NOT_FOUND, a
        TypeError is raised.  With this set, the iteration will act as
        if this was an empty array. :::

            >>> from magic_dot import MagicDot
            >>> x = MagicDot(1)
            >>> for y in x.nonexistent:
            >>>    ...
            (Raises TypeError)
            >>> x = MagicDot(1).iter_nf_as_empty()
            >>> for y in x.nonexistent:
            >>>    ...
            (Skips the contents of the for loop.)

        Args:
            iter_nf_as_empty: Enable or Disable

        Returns:
            If the iter_nf_as_empty changes, a new MagicDot will be returned.  Otherwise,
            this returns self.
        """
        if self.__iter_nf_as_empty == iter_nf_as_empty:
            return self
        else:
            return self.__create_child(self.__data, iter_nf_as_empty=iter_nf_as_empty)


    def get(self, not_found: Any = NOT_FOUND):
        """Gets the encapsulated data in this MagicDot.

        This is either the encapsulated data or NOT_FOUND if extraction 
        failed.

        Args:
           default: Selects what to return if the encapsulated data was NOT_FOUND.

        Returns:
            The encaapsulated data in this MagicDot instance.
        """

        if self.__data is NOT_FOUND:
            return not_found
        else:
            return self.__data

    def pluck(self, name: str):
        """Extracts **name** from an encapsulated data (which must be iterable) into an array.

        For each item in the encapsulated data iterable, extract the named attribute
        or key.  If they are not available, either extract NOT_FOUND or raise an exception
        depending on the current .exception() configuration.

        If the encapsulated date is not iterable and not NOT_FOUND, a TypeError will be raised.

        If the encapsulated data is NOT_FOUND, either raise a TypeError, or return an empty list
        depending on the .iter_nf_as_empty() setting.

        Args:
            text: The attribute or key to pluck from the array.

        Returns:
            A new MagicDot containing the resulting array with plucked data.            
        """        

        data = []
        if not (self.__data == NOT_FOUND and self.__iter_nf_as_empty):
            for x in self.__data:
                try:
                    d = getattr(x, name)
                except AttributeError:
                    try:
                        d = x[name]
                    except (AttributeError, KeyError, TypeError):
                        if self.__exception:
                            raise NotFound from None
                        else:
                            d = NOT_FOUND
                data.append(d)

        return self.__create_child(data)
    
