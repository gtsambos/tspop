.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   simulationsetup
   basicusage
   ideas
   examples
   modules


About ``tspop``
===============

Suppose your genealogical ancestors can be partitioned into distinct populations (represented here by different colours):

.. image:: static/admixture.png
   :scale: 50 %
   :alt: alternate text
   :align: center

This is typically reported as global and local ancestry:

.. image:: static/local-global-ancestry.png
   :scale: 50 %
   :alt: alternate text
   :align: center

Using ``msprime`` and ``SLiM``,
you can simulate under detailed models of migration and population structure.
This is the documentation for ``tspop``,
a lightweight package that makes it easier for you to extract 
information about population-based ancestry from these simulations.

.. note::
	Add link to preprint/note when it's written.

Under the hood, ``tspop`` relies on

  * the ``tskit`` package to efficiently extract the population-based information in the simulated datasets.
  * the ``pandas`` package to provide user-friendly, interpretable output.

First steps
-----------

  * Head to the :ref:`installation` page to install ``tspop`` on your computer.
  * Population-based ancestry is **not well-defined** without some notion of a *census time*. Read :ref:`simulationsetup` to see how to design your simulations to ensure they will work with ``tspop``.
  * Flick through the :ref:`examples` to see ``tspop`` in action.
  * Check out :ref:`ideas` to learn more about why ``tspop`` is so efficient.