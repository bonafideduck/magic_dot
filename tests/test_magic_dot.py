#!/usr/bin/env python

"""Tests for `magic_dot` package."""

import pytest
from collections import namedtuple

from magic_dot import MagicDot
from magic_dot import NOT_FOUND
from magic_dot.exceptions import NotFound


def test_can():
    """Test that dict key is accessible as a hash ."""
    md = MagicDot({"num": 1})
    assert md.num.get() == 1


def test_yet():
    """Test NOT_FOUND is returned."""
    md = MagicDot({"num": 1})
    assert md.buba.get() is NOT_FOUND


def test_other():
    """Test supplied default is returned for NOT_FOUND"""
    md = MagicDot({"num": 1})
    assert md.bubba.get("something") == "something"

def test_coat():
    """Test that attributes are extracted first."""
    class AttrKey(dict):
        a = 7
    ak = AttrKey()
    ak['a'] = 8
    md = MagicDot(ak)
    assert md.a.get() == 7

def test_ride():
    """Test that indexed processing happens by default."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([nt, None, nt])
    assert md[1].get() is None


def test_both():
    """Test that exception is enabled with init."""
    md = MagicDot({}, exception=True)
    with pytest.raises(NotFound):
        md.nonexistent.get()


def test_been():
    """Test that exception is enabled with exception."""
    md = MagicDot({})
    with pytest.raises(NotFound):
        md.exception().nonexistent


def test_curve():
    """Test that exception does not affect the get after NOT_FOUND is detected."""
    md = MagicDot({})
    md.nonexistent.exception().get()

def test_pie():
    """Test that TypeError is raised when iterating over non-data"""
    md = MagicDot(1)
    with pytest.raises(TypeError):
        [x for x in md]

def test_cat():
    """Tests that TypeError is raised for valid non-iterable when iter_nf_as_empty() is set"""
    md = MagicDot(1, iter_nf_as_empty=True)
    with pytest.raises(TypeError):
        [x for x in md]

def test_atom():
    """Tests that TypeError is raised for NOT_FOUND by default"""
    md = MagicDot(1).nonexistent
    with pytest.raises(TypeError):
        [x for x in md]

def test_lesson():
    """Tests that NOT_FOUND returns empty generator with iter_nf_as_empty"""
    md = MagicDot(1, iter_nf_as_empty=True).nonexistent
    assert [x for x in md] == []

def test_layers():
    """Tests that NOT_FOUND returns empty generator with iter_nf_as_empty()"""
    md = MagicDot(1).nonexistent.iter_nf_as_empty()
    assert [x for x in md] == []

def test_trace():
    """Tests ability to walk iterable data."""
    md = MagicDot([None, 1, 2])
    expected = [None, 1, 2]
    for x in md:
        assert x.get() == expected.pop(0)

def test_sign():
    """Tests ability to walk iterable data."""
    md = MagicDot([None, 1, 2])
    expected = [None, 1, 2]
    for x in md:
        assert x.get() == expected.pop(0)

def test_sign():
    """Tests pluck of attributes and nonexistent data."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([nt, None, nt])
    assert md.pluck("x").get() == [1, NOT_FOUND, 1] 

def test_money():
    """Tests pluck of keys and nonexistent data."""
    d = {"x": 1}
    md = MagicDot([d, None, d])
    assert md.pluck("x").get() == [1, NOT_FOUND, 1]

def test_whistle():
    """Tests pluck of nonexistent data raises TypeError"""
    md = MagicDot(1)
    with pytest.raises(TypeError):
        md.nonexistent.pluck('z')

def test_neighborhood():
    """Tests that pluck of nonexistent data with .iter_nf_as_empty returns empty."""
    md = MagicDot(1)
    assert md.nonexistent.iter_nf_as_empty().pluck('whatevs').get() == []

def test_vote():
    """Tests that pluck of noniterable gives type_error"""
    md = MagicDot(1)
    with pytest.raises(TypeError):
        md.pluck('z')

def test_vote():
    """Tests that pluck of noniterable gives type_error even if .iter_nf_as_empty is set."""
    md = MagicDot(1)
    with pytest.raises(TypeError):
        md.iter_nf_as_empty().pluck('z')

def test_yellow():
    """Test that a pluck of NOT_FOUND data raises an NotFound exception if .exception is set"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([nt, None, nt])
    with pytest.raises(NotFound):
        md.exception().pluck("x")

def test_supply():
    """Test that boolean math is not allowed with magic_dot."""
    md = MagicDot(1)
    with pytest.raises(RuntimeError):
        not md

def test_important():
    """Test that boolean math is not allowed on NOT_FOUND"""
    md = MagicDot(1)
    with pytest.raises(RuntimeError):
        not md.nonexistent.get()

def test_in():
    """Test that repr for NOT_FOUND works nicely (for documentation)."""
    md = MagicDot(1)
    assert repr(md.nonexistent.get()) == "magic_dot.NOT_FOUND"

def test_gate():
    """Test that setting exception creates a new md"""
    md = MagicDot(1)
    assert md is not md.exception()

def test_bowl():
    """Test that setting exception twice does note create a new md"""
    md = MagicDot(1, exception=True)
    assert md is md.exception()

def test_solve():
    """Test that setting iter_nf_as_empty creates a new md"""
    md = MagicDot(1)
    assert md is not md.iter_nf_as_empty()

def test_reader():
    """Test that setting iter_nf_as_empty twice does note create a new md"""
    md = MagicDot(1, iter_nf_as_empty=True)
    assert md is md.iter_nf_as_empty()