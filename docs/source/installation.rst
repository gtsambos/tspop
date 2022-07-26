.. _installation:

Installation
============

``tspop`` is available on `PyPi <https://pypi.org/>`_ for
installation with ``pip``:

.. code-block:: bash

    pip install tspop 

If you absolutely must use the most up-to-date code,
you can do it by cloning the ``git`` repository,

.. code-block:: bash

    git clone https://github.com/gtsambos/tspop


navigating into the root directory,

.. code-block:: bash

    cd tspop


and installing it like this:

.. code-block:: bash

    pip install .

Developer installation
----------------------

To install ``tspop`` in addition to the packages needed to develop and run tests,
perform the first two steps above in your virtual environment,
then run the following command:

.. code-block:: bash

    pip install .[dev]

Compiling the documentation
---------------------------

.. note::
	Finish later.

.. code-block:: bash

	cd docs/source
	make clean
	make html
