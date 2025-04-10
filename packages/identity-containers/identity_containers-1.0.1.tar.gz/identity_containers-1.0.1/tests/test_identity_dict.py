from __future__ import annotations

import pytest

from identity_containers import IdentityDict


def test_mutable_keys():
    foo = []
    bar = []

    idict = IdentityDict([(foo, 1), (bar, 2)])

    assert len(idict) == 2
    assert idict[foo] == 1
    assert idict[bar] == 2

    foo.append("hi")
    assert idict[foo] == 1


def test_del_existing_key():
    idict = IdentityDict({1: "a", 2: "b", 3: "c"})
    del idict[2]

    assert 2 not in idict


def test_del_nonexistent_key():
    idict: IdentityDict[int, int] = IdentityDict()

    with pytest.raises(KeyError):
        del idict[3]


def test_iteration():
    idict = IdentityDict({1: "a", 2: "b", 3: "c"})
    assert set(idict.keys()) == {1, 2, 3}
    assert set(idict.values()) == {"a", "b", "c"}
    assert set(idict.items()) == {(1, "a"), (2, "b"), (3, "c")}


def test_update():
    idict = IdentityDict({1: "a", 2: "b", 3: "c"})
    idict.update({4: "d", 5: "e"})

    assert set(idict.items()) == {(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")}


def test_repr():
    idict = IdentityDict([([], "a"), ("b", {})])
    assert repr(idict) == "IdentityDict([([], 'a'), ('b', {})])"
