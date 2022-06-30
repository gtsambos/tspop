
About ``tspop``
===============

This is the documentation for ``tspop``,
a lightweight package that helps you extract information about population-based ancestry
from tree sequences simulated with ``msprime`` and ``SLiM``.

.. note::
	Add link to preprint/note when it's written.

We designed ``tspop`` to make it easier for you to extract information
about population-based ancestry in simulated genetic datasets.
Under the hood, ``tspop`` relies on

  * the ``tskit`` package to efficiently extract the population-based information in the simulated datasets
  * the ``pandas`` package to provide user-friendly, interpretable output

First steps
-----------

  * Head to the :ref:`installation` page to install ``tspop`` on your computer.
  * Population-based ancestry is **not well-defined** without some notion of a *census time*. Read :ref:`simulationsetup` to see how to design your simulations to ensure they will work with ``tspop``.
  * Flick through the :ref:`examples` to see ``tspop`` in action.
  * Check out :ref:`ideas` to learn more about why ``tspop`` is so efficient.

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


Basic usage
===========

.. note::
   Do later.

.. _simulationsetup:

:doc:`simulationsetup`

The ideas behind ``tspop``
==========================

:doc:`ideas`

.. _examples:

Examples
========
