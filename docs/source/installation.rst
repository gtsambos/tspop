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
perform the first two steps above, then run the following command:

.. code-block:: bash

    pip install -e .[dev]

I recommend developing `tspop` in a virtual environment like a ![conda environment](https://conda.io/projects/conda/en/latest/index.html).

Running the tests
-----------------

The test suite uses the ![`pytest`](https://docs.pytest.org/en/7.2.x/) module.

.. code-block:: bash

    pytest tests

You can run specific classes or tests in specific test files:

.. code-block:: bash

    pytest tests/test_tspop.py::TestIbdSquash

To get printed output from the tests, use the `s` flag:

.. code-block:: bash

    pytest -s tests/test_tspop.py::TestIbdSquash.test_basic

.. code-block:: bash

    pytest tests/test_tspop.py::TestIbdSquash.test_basic

Compiling the documentation
---------------------------

.. note::
	Finish later.

.. code-block:: bash

	cd docs
	make clean
	make html
