# multiset-key-dict

This small library implements a mapping-like object whose keys are taken to be
unordered multisets (Counters, bags), regardless of the type of the actual
indexes used.

## Example

Create a `MultisetKeyDict` and insert an element for the set {1, 3, 5}.

```python
from multiset_key_dict import MultisetKeyDict
mskd = MultisetKeyDict()
mskd[[1, 3, 5]] = 19
```

Access the element just added.

```python
# In a different order.
print(mskd[[3, 5, 1]]) # 19
# With a different type of collection.
print(mskd[{3, 5, 1}]) # 19
```

`__iter__` iterates over items in the `MultisetKeyDict`, *viewed as frozensets*
(i.e., not accounting for multiplicity).

```python
# Add more data.
mskd[[1]] = 9
mskd[[5, 6]] = 12
print(list(mskd)) # [(frozenset({1, 3, 5}), 19), (frozenset({1}), 9), (frozenset({5, 6}), 12)]
```

To iterate over key-value pairs where the keys are the `FrozenMultiset` objects
that act as the true keys in the structure, use `multiset_iter` or `items`
methods instead.

```python
msked[[1, 1]] = 90
print(list(mskd))
# [(frozenset({1, 3, 5}), 19), (frozenset({1}), 9), (frozenset({5, 6}), 12),
# (frozenset({1}), 90)]

print(list(mskd.multiset_iter()))
# [(FrozenMultiset({(3, 1), (1, 1), (5, 1)}), 19), 
#  (FrozenMultiset({(1, 1)}), 9),
#  (FrozenMultiset({(6, 1), (5, 1)}), 12),
#  (FrozenMultiset({(1, 2)}), 90)]
```

To get the keys as `frozenset` objects, use `set_keys`. To get the keys as
`FrozenMultiset` objects, use `multiset_keys` or `keys`.

It's sometimes useful to get the set of *elements* of the keys. For that, you
can use the `key_elements` method.

```python
print(mskd.key_elements()) # frozenset({1, 3, 5, 6})
```
