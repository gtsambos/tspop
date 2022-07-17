.. _basicusage:

Basic usage
===========

.. note::
   **Ensure** that your simulated tree sequence follows the guidelines mentioned in :ref:`simulationsetup`.


Here's a sample tree sequence simulated with msprime.
Note the census time at 100.01:

.. code-block:: python

   import msprime

   pop_size = 500
   sequence_length = 1e7
   seed = 98765
   rho = 3e-8

   # Make the Demography object.
   demography = msprime.Demography()
   demography.add_population(name="RED", initial_size=pop_size)
   demography.add_population(name="BLUE", initial_size=pop_size)
   demography.add_population(name="ADMIX", initial_size=pop_size)
   demography.add_population(name="ANC", initial_size=pop_size)
   demography.add_admixture(
       time=100, derived="ADMIX", ancestral=["RED", "BLUE"], proportions=[0.5, 0.5]
   )
   demography.add_census(time=100.01) # Census is here!
   demography.add_population_split(
       time=1000, derived=["RED", "BLUE"], ancestral="ANC"
   )

   # Simulate.
   ts = msprime.sim_ancestry(
       samples={"RED": 0, "BLUE": 0, "ADMIX" : 2},
       demography=demography,
       random_seed=seed,
       sequence_length=sequence_length,
       recombination_rate=rho
   )

Apply :meth:`tspop.get_pop_ancestry` to get a :class:`tspop.PopAncestry` object.

.. code-block:: python

   import tspop

   pa = tspop.get_pop_ancestry(ts, census_time=100.01)


Use ``print`` to see a summary of the information held within the object.

.. code-block:: python

   print(pa)

   > PopAncestry summary 
   >
   > Number of ancestral populations:    2
   > Number of sample chromosomes:       4
   > Number of ancestors:          118
   > Total length of genomes:      40000000.000000
   > Ancestral coverage:        40000000.000000

The ancestral information itself is inside two tables.
The :attr:`tspop.PopAncestry.squashed_table` shows tracts of ancestry:

.. code-block:: python

   st = pa.squashed_table
   print(st)

   >     sample       left       right  population
   > 0        0        0.0    419848.0           0
   > 1        0   419848.0    483009.0           1
   > 2        0   483009.0   1475765.0           0
   > 3        0  1475765.0   2427904.0           1
   > 4        0  2427904.0   3635390.0           0
   > ..      ...        ...         ...       ...         ...
   > 55       3  7369409.0   7596783.0           1
   > 56       3  7596783.0   8289015.0           0
   > 57       3  8289015.0   8918727.0           1
   > 58       3  8918727.0  10000000.0           0


The :attr:`tspop.PopAncestry.ancestry_table` shows a superset of this information: tracts
of ancestry, and the ancestor at the census time who contributed
each tract.
Each row of the squashed table above can be obtained by 'gluing together' rows of the ancestry table.

.. code-block::  python

   at = pa.ancestry_table
   print(at)

   >      sample       left       right  ancestor  population
   > 0         0        0.0     33027.0        74           0
   > 1         0    33027.0    155453.0        33           0
   > 2         0   155453.0    290542.0        46           0
   > 3         0   290542.0    419848.0        18           0
   > 4         0   419848.0    483009.0        83           1
   > ..      ...        ...         ...       ...         ...
   > 133       3  8672850.0   8849756.0        95           1
   > 134       3  8849756.0   8918727.0       131           1
   > 135       3  8918727.0   9165035.0        44           0
   > 136       3  9165035.0   9176562.0        47           0
   > 137       3  9176562.0  10000000.0        58           0

Both the :attr:`tspop.PopAncestry.squashed_table` and the :attr:`tspop.PopAncestry.ancestry_table` are pandas dataframes,
so can be analysed using standard operations.

Example: calculating global ancestry
************************************

For instance, we could get the sum of all regions inherited from an
ancestor in population 0 like this.
We'll first subset the :attr:`tspop.PopAncestry.squashed_table` to only those tracts inherited from an ancestor in population 0:

.. code-block::  python

   st0 = st[st.population == 0]
   print(st0)

   >     sample       left       right  population
   > 0        0        0.0    419848.0           0
   > 2        0   483009.0   1475765.0           0
   > 4        0  2427904.0   3635390.0           0
   > 6        0  4606954.0   6277367.0           0
   > ..      ...        ...         ...       ...         ...
   > 52       3  7043989.0   7134130.0           0
   > 54       3  7362300.0   7369409.0           0
   > 56       3  7596783.0   8289015.0           0
   > 58       3  8918727.0  10000000.0           0

By summing the tract lengths in the rows,
we get the length of the tracts from population 0:

.. code-block:: python

   pop0_lengths = sum(st0.right - st0.left)
   print(pop0_lengths)

   > 23278398.0

Dividing this by the sum of the genomic lengths in the :class:`tspop.PopAncestry` object gives the proportion of the genomes that were inherited from
individuals in population 0, with reference to the ancestors present at the census time:

.. code-block:: python

   print(pop0_lengths/pa.total_genome_length)

   > 0.58195995

   
   


