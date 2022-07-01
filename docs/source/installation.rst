.. _installation:

Installation
============

``tspop`` will soon be available on `PyPi <https://pypi.org/>`_ for
installation with ``pip``. Until then, you can use it locally by
cloning the ``git`` repository,

.. code-block:: bash

    git clone https://github.com/gtsambos/tspop


navigating into the root directory,

.. code-block:: bash

    cd tspop


and installing it like this:

.. code-block:: bash

    pip install -e

Developer installation
----------------------

To install ``tspop`` in addition to the packages needed to develop and run tests,
perform the first two steps above in your virtual environment,
then run the following command:

.. code-block:: bash

    pip install -e .[dev]	