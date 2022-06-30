.. _ideas:

The ideas behind ``tspop``
==========================

Simulated tree sequences contain richly detailed information about local ancestry: any sample node that descends from a node in a given population at some genomic location will have ancestry with the population at that location.

However, for realistically large and complicated simulations, it is difficult to recover this information from the overall genealogies.
A visually intuitive way to do this is to locate each sample haplotype on each tree and trace a path up the tree until an ancestral node from one of the populations of interest is reached.

Unfortunately, this approach will be quite inefficient. Any genealogical feature that is shared between different haplotypes, or across different regions of the genome, will be processed separately for each sample and each tree. Given the substantial correlations in genealogy that typically exist between individuals, and across genomes, this approach would require many repetitive operations.

To extract local ancestry from a tree sequence, there are several essential steps:

1. Make a record of which nodes belong to ancestors in the populations of interest.
2. For each genomic segment belonging to a present-day sample, trace a path upwards through the trees to determine which of the nodes in the first step are ancestral to each subsegment.
3. Look up the population `p` that each ancestral node `a` belongs to. Then any segments that descend from `a` have local ancestry with population `p`.

Step 2 is potentially complicated and inefficient. This is the operation performed efficiently by the `link-ancestors` method in `tskit`.
Essentially, `link-ancestors` performs a 'simplification' of the tree
sequence so that relationships between samples and ancestors of interest
are shown directly.

.. note::
	Algorithmic details are in the preprint.

