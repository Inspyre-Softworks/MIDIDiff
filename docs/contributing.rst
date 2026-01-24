Contributing
============

We welcome contributions! This guide will help you get started with contributing
to MIDIDiff.

Development Setup
-----------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/tayjaybabee/MIDIDiff.git
      cd MIDIDiff

2. Install Poetry if you haven't already:

   .. code-block:: bash

      pip install poetry

3. Install dependencies:

   .. code-block:: bash

      poetry install

4. Install development dependencies (including Sphinx for documentation):

   .. code-block:: bash

      poetry install --with dev

Contribution Guidelines
-----------------------

Code Contributions
~~~~~~~~~~~~~~~~~~

Please see `CONTRIBUTING.md <https://github.com/tayjaybabee/MIDIDiff/blob/main/CONTRIBUTING.md>`_
for detailed guidelines on:

* How to contribute code and documentation
* Changelog update requirements
* Development setup
* Pull request process

All contributions with user-facing changes must update the
`CHANGELOG.md <https://github.com/tayjaybabee/MIDIDiff/blob/main/CHANGELOG.md>`_ file.

Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The generated HTML documentation will be in ``docs/_build/html/``.

To view the documentation, open ``docs/_build/html/index.html`` in your browser.

Clean Build
~~~~~~~~~~~

To clean the build directory and rebuild from scratch:

.. code-block:: bash

   cd docs
   make clean
   make html

Testing Documentation
~~~~~~~~~~~~~~~~~~~~~

To check for broken links and other issues:

.. code-block:: bash

   cd docs
   make linkcheck

Read the Docs
-------------

This project is configured for automatic documentation building on
`Read the Docs <https://readthedocs.org/>`_. Documentation is built
automatically when changes are pushed to the repository.

License
-------

MIDIDiff is licensed under the MIT License. See the
`LICENSE.md <https://github.com/tayjaybabee/MIDIDiff/blob/main/LICENSE.md>`_
file for details.
