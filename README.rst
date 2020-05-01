Magic Dot
*********


.. image:: https://img.shields.io/pypi/v/magic_dot.svg
        :target: https://pypi.python.org/pypi/magic_dot

.. image:: https://img.shields.io/pypi/dm/magic_dot.svg
        :target: https://pypi.python.org/pypi/magic_dot

.. image:: https://github.com/bonafideduck/magic_dot/workflows/Sanity/badge.svg
        :target: https://github.com/bonafideduck/magic_dot/actions?query=branch%3Amaster+workflow%3A%22Sanity%22

.. image:: https://readthedocs.org/projects/magic-dot/badge/?version=latest
        :target: https://magic-dot.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Library that allows deep extraction of layered data structures (like JSON).


* Free software: BSD license
* Documentation: https://magic-dot.readthedocs.io.


Introduction
============

Magic Dot encapsulates data to allow the versatile extraction of its contents.
It is easier to use than ``setdefault`` or ``try:`` ``except`` that typical
extraction from a structured like JSON.  Consider the following simplified JSON 
snipppet curl https://api.github.com/events: ::

  import json
  data = json.loads("""
    [
      {
        "type": "PushEvent",
        "payload": {
          "commits": [
            {
              "author": {
                "name": "Bubba"
    }}]}}]
  """)

``magic_dot`` can retrieve the first name of the first commit, with a default of "nobody" if any
part of that chain is missing with the the following: ::

  from magic_dot import MagicDot, NOT_FOUND
  name = MagicDot(data)[0].payload.commits[0].author.name.get("nobody")

Since the incoming JSON can't be trusted, without magic_dot, you have to verify that 
each layer is there.  This can be done with a ``try:`` ``except``, nearly as
efficiently, but it is more verbose. ::

  try:
    name = data[0]['payload']['commits'][0]['author']['name']
  except (IndexError, KeyError):
    name = "nobody"

Other features, like pluck, selective exceptions,
attribute support, and iteration can lead to cleaner code.

Features
========

Forgiving NOT_FOUND Handling
----------------------------

Manipulations of the MagicDot structure will raise no exceptions
when one of the attributes or keys are not found.  Instead it delays
this until the ``get()`` call that extracts the data at the end.
When the ``get()`` is called, there are three ways of handling
missing data:

**Default is to return magic_dot.NOT_FOUND** ::

  >>> md.nonexistent.get()
  magic_dot.NOT_FOUND

**You can request a default value for magic_dot.NOT_FOUND** ::

  >>> md.nonexistent.get('bubba')
  'bubba'

**Or you can enable exceptions when referencing the nonexistent data** ::

    >>> md.exception().nonexistent
    ---------------------------------------------------------------------------
    NotFound                                  Traceback (most recent call last)

Exceptions are not enabled by default.  They can be enabled during creation
I.E ``MagicDot(data, exception=True)`` and switched on and off with the 
``MagicDot::exception(exception=False)`` method.

Dict and List Item Handling
---------------------------

When a `md[item]` is encountered, data will be extracted as follows:

1. If ``md.__data[item]`` exists, that is used.
2. If ``md.__data.item`` attribute exists it is used.
3. If ``.exception()`` is enabled, a NotFound exception is raised.
4. Otherwise ``md.NOT_FOUND`` is assigned to the resulting encapsulated data.

Attribute Handling
------------------

When a ``md.key`` is supplied data will be extracted as follows:

1. If ``md.__data.key`` attribute exists it is used.
2. If ``md.__data[key]`` item exists, it is used.
3. If ``.exception()`` is enabled, a NotFound exception is raised.
4. Otherwise ``md.NOT_FOUND`` is assigned to the resulting ``md.__data``.


Iteration Support
-----------------

If the currently encapsulated data is an iterable, MagicDot supports iterating
over the contained data with the resulting iteration being a MagicDot wrapper
around the iterated data.

  >>> from collections import namedtuple
  >>> data = [1, {'x': 2}, namedtuple('x', 'x')(3)]
  >>> for md in MagicDot(data):
  ...   print(md.get())
  1
  {'x': 2}
  x(x=3)

By default, if an attempt is made to iterate over ``NOT_FOUND`` data, a ``TypeError``
will be raised.  The iteration code can be changed to instead return an empty list. :::

  >> md = MagicDot(1, iter_nf_as_empty=True)
  >> for x in md.nonexistent:
  ..   print(md.get())
  (prints nothing)


Other Operators
---------------

Currently, there is one additional operator, ``MagicDot::pluck()``, which if
the encapsulated data is a list, it will attempt to extract a named attribute
or key from the entire list.  The returned value is a MagicDot with the new plucked list.


Future Enhancement
==================

Future enhancements will be to support many of the `Underscore js`_ array and collection capabilities
like ``compact``, ``reject``, and ``count``.

.. _`Underscore js`: https://underscorejs.org/#arrays


Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
