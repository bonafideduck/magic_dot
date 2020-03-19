Magic Dot
*********


.. image:: https://img.shields.io/pypi/v/magic_dot.svg
        :target: https://pypi.python.org/pypi/magic_dot

.. image:: https://img.shields.io/travis/bonafideduck/magic_dot.svg
        :target: https://travis-ci.com/bonafideduck/magic_dot

.. image:: https://readthedocs.org/projects/magic-dot/badge/?version=latest
        :target: https://magic-dot.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Library that allows deep extraction of layered data structures (like JSON).


* Free software: BSD license
* Documentation: https://magic-dot.readthedocs.io.


Introduction
============

Magic Dot delays the extraction of data to when you are ready of it.  It
works best with structured data like JSON.  Consider the following simplified JSON 
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

``magic_dot`` has a process of wrapping the data for easier extraction without
the need for complex ``setdefault`` or ``try:`` ``except``.  For example, to
retrieve the first name of the first commit, you would do the following: ::

  from magic_dot import MagicDot, NOT_FOUND
  md = MagicDot(data)
  md[0].payload.commits[0].author.name.get()
  if name is NOT_FOUND:
    print("handle error")
  else:
    print("success")

Since the incoming JSON can't be trusted, you have to verify that each layer is
there.  This can be done with a ``try:`` ``except``, nearly as efficiently, but
it is more verbose. ::

  try:
    name = md[0]['payload']['commits'][0]['author']['name']
  except (IndexError, KeyError):
    print("handle error")
  else:
    print("success")

In the above instance, it is a tossup between MagicDot and ``try:`` ``except``.
Other features, like list extraction, default handling, selective exceptions,
and attributes support can lead to cleaner code.

Features
========

For all the code examples, we will assume the following code has already been run: ::

  import json
  from magic_dot import MagicDot, NOT_FOUND
  from magic_dot.exceptions import NotFound
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
  md = MagicDot(data)

Forgiving NOT_FOUND Handling
----------------------------

Manipulations of the MagicDot structure will raise no exceptions
when one of the attributes or keys are not found.  Instead it delays
this until the ``get()`` call that extracts the data at the end.
When the ``get()`` is called, there are three ways of handling
missing data:

**Default is to return ``magic_dot.NOT_FOUND``** ::

  In [1]: md.nonexistent.get()
  Out[1]: magic_dot.NOT_FOUND

**You can request a default value for ``magic_dot.NOT_FOUND``** ::

  In [2]: md.nonexistent.get('bubba')
  Out[2]: 'bubba'

**Or raise an exception for NOT_FOUND** ::

    In [3]: md.exception().nonexistent.get()
    ---------------------------------------------------------------------------
    NotFound                                  Traceback (most recent call last)

Exceptions are not enabled by default.  They can be enabled during creation
I.E ``MagicDot(data, exception=True)`` and switched on and off with the 
``MagicDot::exception(exception=True)`` method.

Dict and List Item Handling
---------------------------

When a `md[item]` is encountered, data will be extracted as follows:

1. If ``md.__data[item]`` exists, that is used.
2. If ``md.__data.item`` attribute exists it is used.
3. If `lists` is enabled and item is not an int, lists will be searched (see List Support below).
4. Otherwise ``md.NOT_FOUND`` is assigned to the resulting ``md.__data``.

Attribute Handling
------------------

When a ``md.key`` is supplied data will be extracted as follows:

1. If ``md.__data.key`` attribute exists it is used.
2. If ``md.__data[key]`` item exists, it is used.
3. If `lists` is enabled, lists will be search (see List Support below).
4. Otherwise ``md.NOT_FOUND`` is assigned to the resulting ``md.__data``.

List Support
------------

When ``MagicDot(data, lists=True)`` is enabled (which is the default), extra
list support is enabled.  Please note that the **lists** is short for **list s**\upport
and not multiple lists.  With list support, if a attribute or item access would return NOT_FOUND
and the data is a list, the contents of that list will be searched using attribute(see above).
If anything is found, then a list will be returned.

As an example, given this data: ::

  In [1]: from collections import namedtuple
  In [2]: data = [1, {'x': 2}, namedtuple('x', 'x')(3)]
  In [3]: data[0]
  Out[3]: 1
  In [4]: data[1]['x']
  Out[4]: 2
  In [5]: data[2].x
  Out[5]: 3

The following will be returned with the first item not expanding becuase it is an integer. ::

  In [6]: md = MagicDot(data)
  In [7]: md.x.data()
  Out[7]: [magic_dot.NOT_FOUND, 2, 3]

With list processing disabled, ``NOT_FOUND`` will be returned. ::

  In [6]: md = MagicDot(data, lists=False)
  In [7]: md.x.get()
  Out[7]: magic_dot.NOT_FOUND

If a default is supplied for the get, the ``NOT_FOUND``\(s) in the underlying lists will be expanded. ::

  In [6]: md = MagicDot(data)
  In [7]: md.x.get('bubba')
  Out[7]: ['bubba', 2, 3]

If data is referenced with list processing, but list procesing is turned off before
the ``get()``, the list ``NOT_FOUNDS``\(s) will not be replaced. ::

  In [6]: md = MagicDot(data)
  In [7]: md.x.lists(False).get('bubba')
  Out[7]: [magic_dot.NOT_FOUND, 2, 3]

Future Enhancement
==================

These are some ideas that may be added in future versions:

* ``.compact(remove=[NOT_FOUND, None])``: removes MagicDot list items that are ``NOT_FOUND`` or ``None``
* ``.sort(key=None, reverse=False)``: returns MagicDot with a new sorted list
* ``.delete_if(func)``: Returns a new MagicDot with anything in delete removed if true.
* ``.find(func)``: Returns a new MagicDot with the first match.
* ``.uniq()``: Returns uniq list values.
* I.E. a wide variaty of variations like `Underscore js`_ or `Ruby Arrays`_

.. _`Underscore js`: https://underscorejs.org/#arrays
.. _`Ruby Arrays`: https://ruby-doc.org/core-2.7.0/Array.html


Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
