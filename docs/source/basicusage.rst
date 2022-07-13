.. _basicusage:

Basic usage
===========

.. note::
   **Ensure** that your simulated tree sequence follows the guidelines mentioned in ref:`simulationsetup`.


Here's a sample tree sequence simulated with msprime.
Note the census time at 100.01:

.. code-block:: python

   import msprime

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
       random_seed=1011,
       sequence_length=100000,
       recombination_rate=3e-8
   )

Apply ``tspop.get_pop_ancestry()`` to get a PopulationAncestry object.

.. code-block:: python

   import tspop

   pa = tspop.get_pop_ancestry(ts, census_time=100.01)


Use ``print`` to see a summary of the information held within the object.

.. code-block:: python

   print(pa)

   >>> PopAncestry summary
   >>>
   >>> Number of ancestral populations:    2
   >>> Number of sample chromosomes:       4
   >>> Number of ancestors:          32
   >>> Total length of genomes:      40000000.000000
   >>> Ancestral coverage:        40000000.000000

The ancestral information itself is inside two tables.
The ``squashed_table`` shows tracts of ancestry:

.. code-block:: python

   st = pa.squashed_table
   print(st)

   >      sample       left       right  population
   > 0        0        0.0     80052.0           0
   > 1        0    80052.0   1990898.0           1
   > 2        0  1990898.0   8285048.0           0
   > 3        0  8285048.0  10000000.0           1
   > 4        1        0.0    217658.0           1
   > 5        1   217658.0   1384892.0           0
   > 6        1  1384892.0   3495144.0           1
   > 7        1  3495144.0   9137452.0           0
   > 8        1  9137452.0   9365227.0           1
   > 9        1  9365227.0  10000000.0           0
   > 10       2        0.0   3074507.0           0
   > 11       2  3074507.0   3705418.0           1
   > 12       2  3705418.0   7822068.0           0
   > 13       2  7822068.0  10000000.0           1
   > 14       3        0.0   4599467.0           1
   > 15       3  4599467.0   4605356.0           0
   > 16       3  4605356.0   8910468.0           1
   > 17       3  8910468.0  10000000.0           0

The ``ancestry_table`` shows a superset of this information: tracts
of ancestry, and the ancestor at the census time who contributed
each tract.
Each row of the squashed table above can be obtained by 'gluing together' rows of the ancestry table.

.. code-block::  python

   at = pa.ancestry_table
   print(at)

   >     sample       left       right  ancestor  population
   > 0        0        0.0     80052.0        25           0
   > 1        0    80052.0   1990898.0        30           1
   > 2        0  1990898.0   4198170.0        16           0
   > 3        0  4198170.0   4217014.0        21           0
   > 4        0  4217014.0   4916302.0         8           0
   > 5        0  4916302.0   6067459.0        12           0
   > 6        0  6067459.0   7189580.0        11           0
   > 7        0  7189580.0   7547087.0        18           0
   > 8        0  7547087.0   8285048.0        19           0
   > 9        0  8285048.0   8453423.0        27           1
   > 10       0  8453423.0   9583655.0        33           1
   > 11       0  9583655.0  10000000.0        26           1
   > 12       1        0.0    217658.0        37           1
   > 13       1   217658.0   1384892.0         9           0
   > 14       1  1384892.0   3495144.0        34           1
   > 15       1  3495144.0   3732040.0        23           0
   > 16       1  3732040.0   9137452.0        15           0
   > 17       1  9137452.0   9365227.0        31           1
   > 18       1  9365227.0  10000000.0        20           0
   > 19       2        0.0   3074507.0        24           0
   > 20       2  3074507.0   3545810.0        28           1
   > 21       2  3545810.0   3705418.0        29           1
   > 22       2  3705418.0   4217014.0         7           0
   > 23       2  4217014.0   4916302.0         8           0
   > 24       2  4916302.0   6067459.0        12           0
   > 25       2  6067459.0   6844171.0        13           0
   > 26       2  6844171.0   6871827.0         6           0
   > 27       2  6871827.0   7189580.0        17           0
   > 28       2  7189580.0   7547087.0        18           0
   > 29       2  7547087.0   7822068.0        22           0
   > 30       2  7822068.0  10000000.0        32           1
   > 31       3        0.0   4599467.0        36           1
   > 32       3  4599467.0   4605356.0        10           0
   > 33       3  4605356.0   8910468.0        35           1
   > 34       3  8910468.0  10000000.0        14           0

Both the ``squashed_table`` and the ``ancestry_table`` are pandas dataframes,
so can be analysed using standard operations.

Example: calculating global ancestry
************************************

For instance, we could get the sum of all regions inherited from an
ancestor in population 0 like this.
We'll first subset the ``squashed_table`` to only those tracts inherited from an ancestor in population 0:

.. code-block::  python

   st0 = st[st.population == 0]
   print(st0)

   >     sample       left       right  population
   > 0        0        0.0     80052.0           0
   > 2        0  1990898.0   8285048.0           0
   > 5        1   217658.0   1384892.0           0
   > 7        1  3495144.0   9137452.0           0
   > 9        1  9365227.0  10000000.0           0
   > 10       2        0.0   3074507.0           0
   > 12       2  3705418.0   7822068.0           0
   > 15       3  4599467.0   4605356.0           0
   > 17       3  8910468.0  10000000.0           0

By summing the tract lengths in the rows,
we get the length of the tracts from population 0:

.. code-block:: python

   pop0_lengths = sum(st0.right - st0.left)
   print(pop0_lengths)

   > 22105095.0

Dividing this by the sum of the genomic lengths in the PopAncestry object gives the proportion of the genomes that were inherited from
individuals in population 0, with reference to the ancestors present at the census time:

.. code-block:: python

   print(pop0_lengths/pop_table.total_genome_length)

   > 0.552627375

   
   


