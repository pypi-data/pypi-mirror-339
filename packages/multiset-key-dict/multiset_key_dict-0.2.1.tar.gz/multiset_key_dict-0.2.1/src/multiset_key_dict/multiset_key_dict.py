import operator

from collections.abc import Iterable
from typing import  Iterator

from .frozen_multiset import FrozenMultiset

class MultisetKeyDict[KT, VT]:
    """A mapping from frozen (and unordered) multisets to values.

    Although keys are stored as FrozenMultiset objects, the __getitem__ method
    automatically converts any provided argument to a FrozenMultiset, so
    providing a list, tuple, frozenset, etc. will also work.

    This class has no public attributes.
    """
    def __init__(self, mapping = None, mapping_type=dict):
        """Construct a new MultisetKeyDict, optionally from an existing mapping.

        If mapping is a MultisetKeyDict, the constructed MultisetKeyDict will be
        a copy of the existing MultisetKeyDict.

        If mapping is a dict, then the constructed MultisetKeyDict will contain
        the same key-value pairs as mapping, with every key converted to a
        FrozenMultiset.

        If mapping is neither a MultisetKeyDict nor a dict, then the constructor
        will assume that mapping is an iterable of key-value pairs. The
        constructed MultisetKeyDict will contain the same key-value pairs, with
        every key converted to a FrozenMultiset.

        mapping_type allows the caller to construct a MultisetKeyDict with
        a backing mapping of type other than dict.

        Parameters:
            mapping:             Mapping or key-value pairs to add to the dict.
            mapping_type (type): Type of mapping to use for the internal "dict."
        """
        self._dict = mapping_type()
        if mapping is not None:
            try:
                self._dict = mapping_type(mapping.multiset_iter())
            except AttributeError:
                try:
                    self._dict = {
                        FrozenMultiset(k): v for (k, v) in mapping.items()
                    }
                except AttributeError:
                    for k, v in mapping:
                        self._dict[FrozenMultiset(k)] = v

    def __getitem__(self, k : KT) -> VT:
        """Gets the value associated with key k, viewed as a FrozenMultiset."""
        return self._dict[FrozenMultiset(k)]

    def __setitem__(self, k : KT, v : VT):
        """Sets the value associated with key k, viewed as a FrozenMultiset."""
        self._dict[FrozenMultiset(k)] = v

    def __delitem__(self, k : KT):
        """Deletes the key-value pair for key k, viewed as a FrozenMultiset."""
        del self._dict[FrozenMultiset(k)]

    def set_iter(self) -> Iterator[tuple[frozenset[KT], VT]]:
        """Yields items in the MultisetKeyDict, with keys viewed as frozensets.

        The frozenset keys ignore multiplicity of the key elements.
        """
        for k, v in self._dict.items():
            yield frozenset(x[0] for x in k), v

    def multiset_iter(self) -> Iterator[tuple[FrozenMultiset[KT], VT]]:
        """Yields key-value pairs in the MultisetKeyDict.

        Unlike set_iter, key element multiplicity is preserved.
        """
        
        yield from self._dict.items()

    def __iter__(self) -> Iterator[tuple[frozenset[KT], VT]]:
        """Yields items in the MultisetKeyDict, with keys viewed as frozensets.

        Note that the behavior of __iter__ in MultisetKeyDict differs from the
        behavior of __iter__ in the dict class---both keys and values are
        returned here.
        """
        yield from self.set_iter()
 
    def items(self) -> Iterator[tuple[FrozenMultiset[KT], VT]]:
        """Yields key-value pairs in the MultisetKeyDict."""
        return self.multiset_iter()

    def __len__(self) -> int:
        """Get the number of key-value pairs in the MultisetKeyDict."""
        return len(self._dict)

    def __contains__(self, k : Iterable[KT]) -> bool:
        """Returns whether k, viewed as a FrozenMultiset, is a key."""
        return FrozenMultiset(k) in self._dict

    def set_keys(self) -> Iterator[frozenset[KT]]:
        """Yields the keys of this MultisetKeyDict, viewed as frozensets."""
        for k, _ in self.set_iter():
            yield k

    def multiset_keys(self) -> Iterator[FrozenMultiset[KT]]:
        """Yields the keys of this MultisetKeyDict."""
        yield from self._dict.keys()

    def keys(self) -> Iterator[FrozenMultiset[KT]]:
        """Yields the keys of this MultisetKeyDict."""
        return self.multiset_keys()

    def values(self) -> Iterator[VT]:
        """Yields the values of this MultisetKeyDict."""
        yield from self._dict.values()

    def _dict_op(self, op, other):
        new = MultisetKeyDict()
        new._dict = op(self._dict, other._dict)
        return new

    def __or__(self, other):
        """Computes the union of this MultisetKeyDict with other.

        If this MultisetKeyDict and other have the different values for some
        key, the value in other takes precedence.
        """
        return self._dict_op(operator.or_, other)

    def key_elements(self) -> frozenset[KT]:
        """Returns all distinct elements of keys."""
        return frozenset.union(*self.set_keys())

    def __getattr__(self, attr):
        return getattr(self._dict, attr)
