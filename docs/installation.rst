Installation
============

Requirements
------------

* Python 3.11+
* ``mido`` (installed automatically via the project dependencies)
* ``rich`` (optional, for enhanced CLI output)

Installation Methods
--------------------

With Poetry (recommended for development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   poetry install

This installs the core library and all optional dependencies, including the CLI extras.

Build and Install Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   poetry build
   pip install dist/*.whl

For CLI functionality with rich formatting, install with CLI extras:

.. code-block:: bash

   pip install dist/midi_diff-*.whl[cli]

Or install directly from the package:

.. code-block:: bash

   pip install "midi-diff[cli]"

Core Library Only
~~~~~~~~~~~~~~~~~

If you only need the core library without CLI dependencies (e.g., for programmatic use),
install without extras:

.. code-block:: bash

   pip install midi-diff
