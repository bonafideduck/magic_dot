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


def test_square():
    """Test list processing is enabled by default."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt])
    assert md.x.get() == [NOT_FOUND, 1, 1]


def test_two():
    """Test that list processing is disabled from parameter"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt], lists=False)
    assert md.x.get() is NOT_FOUND


def test_carbon():
    """Test that list processing runs when enabled as a call"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt])
    assert md.lists().x.get() == [NOT_FOUND, 1, 1]


def test_weak():
    """Test that list processing is disabled with a parameter"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt])
    assert md.lists(False).x.get() is NOT_FOUND


def test_house():
    """Test that list processing replaces NOT_FOUND with defaults"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt])
    assert md.x.get(0) == [0, 1, 1]


def test_son():
    """Test that lists(False) does not replace a NOT_FOUND in a list NOT_FOUND value with defaults"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt])
    assert md.x.lists(False).get(0) == [NOT_FOUND, 1, 1]


def test_ride():
    """Test that indexed processing happens by default."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([nt, None, nt])
    assert md[1].get() is None


def test_date():
    """Test that indexed processing happens when lists is disabled."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([nt, None, nt])
    assert md.lists(False)[1].get() is None


def test_both():
    """Test that exception is enabled with init."""
    md = MagicDot({}, exception=True)
    with pytest.raises(NotFound):
        md.nonexistent.get()


def test_been():
    """Test that exception is enabled with exception."""
    md = MagicDot({})
    with pytest.raises(NotFound):
        md.exception().nonexistent.get()


def test_curve():
    """Test that exception is enabled with exception after attribute."""
    md = MagicDot({})
    with pytest.raises(NotFound):
        md.nonexistent.exception().get()


def test_hair():
    """Test that exception does not happen with a default."""
    md = MagicDot({}, exception=True)
    assert md.nonexistent.get(0) == 0


def test_hay():
    """Test that exception happens in list processing."""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt], exception=True)
    with pytest.raises(NotFound):
        md.x.get()  # ([NOT_FOUND, 1, 1])


def test_fully():
    """Test that exception does not happen if list processing replaces NOT_FOUND with defaults"""
    nt = namedtuple("NT", "x")(1)
    md = MagicDot([None, nt, nt], exception=True)
    assert md.x.get(0) == [0, 1, 1]
