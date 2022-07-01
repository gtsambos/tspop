.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   simulationsetup
   basicusage
   ideas
   examples

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