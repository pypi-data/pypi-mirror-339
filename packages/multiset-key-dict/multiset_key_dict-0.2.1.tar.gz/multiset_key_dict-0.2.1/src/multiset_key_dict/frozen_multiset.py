from collections import Counter
from collections.abc import Mapping, Set, Iterable
from typing import Optional, Union, Iterator

class FrozenMultiset[T](Set):
    """A class representing an immutable multiset (Counter, bag).

    Unlike Counter, this class does not currently allow one to access the
    multiplicity of an element directly. To obtain the multiplicity of an item,
    one may iterate through the multiset to find the item and its multiplicity.

    Instances of this class have no public attributes.
    """    
    def __init__(self, existing : Optional = None):
        """Construct a new FrozenMultiset, optionally from an existing iterable.

        existing may be an existing FrozenMultiset or an iterable of objects to
        be counted.
        """
        self._set = frozenset()
        try:
            self._set = frozenset(existing._set)
        except AttributeError:
            self._set = frozenset(Counter(existing).items())

    def __contains__(self, k : T) -> bool:
        return k in self._set

    def __iter__(self) -> Iterator[tuple[T, int]]:
        """Yields elements and their multiplicities."""
        return iter(self._set)

    def __len__(self) -> int:
        """Returns the number of distinct elements in this FrozenMultiset."""
        return len(self._set)

    def __repr__(self) -> str:
        return "FrozenMultiset({})".format(repr(set(self._set)))

    def __hash__(self) -> int:
        return hash(self._set)

    def distinct(self) -> frozenset:
        return frozenset(s[0] for s in self._set)

    @classmethod
    def from_counts(
            cls,
            counts : Union[Mapping[T, int], Iterable[tuple[T, int]]]
    ):
        res = cls()
        try:
            res._set = frozenset(counts.items())
        except AttributeError:
            res._set = frozenset(counts)
        return res
