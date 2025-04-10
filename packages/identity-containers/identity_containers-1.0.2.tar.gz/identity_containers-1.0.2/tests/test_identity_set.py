from __future__ import annotations

import pytest

from identity_containers import IdentitySet


def test_mutable_elements():
    foo = []
    bar = []

    iset = IdentitySet([foo, bar])

    assert len(iset) == 2
    assert foo in iset
    assert bar in iset

    foo.append("hi")
    assert foo in iset


def test_remove():
    iset: IdentitySet[int] = IdentitySet()

    with pytest.raises(ValueError):
        iset.remove(3)


def test_clear():
    iset = IdentitySet([1, 2, 3])
    iset.clear()

    assert len(iset) == 0
    assert not iset


def test_discard_existing_item():
    iset = IdentitySet([1, 2, 3])
    iset.discard(2)
    assert 2 not in iset


def test_discard_nonexistent_item():
    iset = IdentitySet([1, 2, 3])
    iset.discard(0)
    assert len(iset) == 3


def test_iteration():
    iset = IdentitySet([1, 2, 3])
    assert set(iset) == {1, 2, 3}


def test_union():
    iset = IdentitySet([1, 2, 3])
    fset: IdentitySet[float] = iset.union([3.5])

    assert set(fset) == {1, 2, 3, 3.5}


def test_repr():
    iset = IdentitySet([[], {}, 3])
    assert repr(iset) == "IdentitySet([[], {}, 3])"
