
import tskit
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class PopAncestry(object):
	"""
	In most cases, this should be created with the :meth:`tspop.get_pop_ancestry` method.
	An object holding local ancestry information, and various summaries of that information.

	:arg left: The array of left coordinates.
	:type left: list(float)
	:arg right: The array of right coordinates.
	:type right: list(float)
	:arg population: The array of population labels.
	:type population: list(int)
	:arg sample_nodes: The list of IDs corresponding to sample nodes.
	:type sample_nodes: list(int)
	:arg sequence_length: The physical length of the region represented.
	:type sequence_length: float

	"""

	def __init__(self, left, right, population, ancestor, child,
		sample_nodes, sequence_length):
		self.left = np.array(left, dtype=np.float64)
		self.right = np.array(right, dtype=np.float64)
		self.population = np.array(population, dtype=np.int32)
		self.ancestor = np.array(ancestor, dtype=np.int32)
		self.sample = np.array(child, dtype=np.int32)
		self._sequence_length = sequence_length
		# self._num_rows = self.__num_rows()
		
		# Create the ancestry tables
		self.ancestry_table = pd.DataFrame(
		data = {
			'left': left,
			'right': right,
			'ancestor' : ancestor,
			'population' : population,
			'sample' : child
		})
		self.ancestry_table.sort_values(
			by=['sample','left'], inplace=True, ignore_index=True)
		# Squashed table
		self.squashed_table = self._squash_ancestry_tracts()
		"""
		A pandas.DataFrame object with column labels ``sample``, ``left``, ``right``, ``population``.
		Each row (``sample``, ``left``, ``right``, ``population``) indicates that over the genomic interval
		with coordinates [``left``, ``right``), the sample node with ID ``sample`` has inherited
		from an ancestral node in the population with ID ``population``.
		Population labels are taken from the specified census time.
		"""
		# Reorder the raw table
		self.ancestry_table = self.ancestry_table[['sample', 'left', 'right', 'ancestor', 'population']]
		"""
		A pandas.DataFrame object with column labels ``sample``, ``left``, ``right``, ``ancestor``, ``population``.
		Each row (``sample``, ``left``, ``right``, ``ancestor``, ``population``) indicates that over the genomic interval
		with coordinates [``left``, ``right``), the sample node with ID ``sample`` has inherited
		from the ancestral node with ID ``ancestor`` in the population with ID ``population``.
		Ancestral nodes and population labels are taken from the specified census time.
		"""

		# Summary attributes. Some are just wrappers for the ts attributes -- needed?
		self.ancestral_pops = list(set(self.squashed_table['population']))
		self.num_ancestral_pops = len(self.ancestral_pops)
		self.samples = sample_nodes
		self.num_samples = len(sample_nodes)
		"""The number of provided samples."""
		self.ancestors = list(set(self.ancestry_table['ancestor']))
		self.num_ancestors = len(self.ancestors)
		"""The number of ancestral haplotypes. Strictly less than or equal to the
		number of inputted ancestral nodes."""
		self.total_genome_length = sequence_length * self.num_samples
		"""Sequence length times the number of samples."""
		self.coverage = self._calculate_coverage()
		"""The proportion of the total genome length with an ancestor in the
		:attr:`tspop.PopAncestry.squashed_table` and :attr:`tspop.PopAncestry.ancestry_table`."""

	def __str__(self):
		ret = """\nPopAncestry summary\n"""
		ret += "Number of ancestral populations: \t{}\n".format(self.num_ancestral_pops)
		ret += "Number of sample chromosomes: \t\t{}\n".format(self.num_samples)
		ret += "Number of ancestors: \t\t\t{}\n".format(self.num_ancestors)
		ret += "Total length of genomes: \t\t{:.6f}\n".format(self.total_genome_length)
		ret += "Ancestral coverage: \t\t\t{:.6f}\n".format(self.coverage)
		return ret[:-1]

	# def __num_rows(self):
	# 	"""
	# 	Returns the number of rows in the table.
	# 	"""
	# 	self._check_row_lengths()
	# 	return len(self.left)

	def _check_row_lengths(self):
		"""
		Checks that the length of each input field is the same.
		"""
		assert len(self.left) == len(self.right)
		assert len(self.right) == len(self.population)
		assert len(self.population) == len(self.sample)

	def _squash_ancestry_tracts(self):
		"""
		Returns a table showing local ancestry only
		(population labels are removed and only contiguous segments
		from the same population are shown.)
		"""
		new_sample = []
		new_left = []
		new_right = []
		new_population = []

		for ind, row in self.ancestry_table.iterrows():
			if ind > 0 and row['left']==new_right[-1] and row['population'] == new_population[-1] and row['sample'] == new_sample[-1]:
				new_right[-1] = row['right']
			else:
				new_sample.append(row['sample'])
				new_left.append(row['left'])
				new_right.append(row['right'])
				new_population.append(row['population'])
				
		squashed_ancestry_table = pd.DataFrame({
			'sample': [int(i) for i in new_sample],
			'left' : new_left,
			'right': new_right,
			'population' : [int(p) for p in new_population]
		})

		return(squashed_ancestry_table)

	def _calculate_coverage(self):
		lengths = self.squashed_table['right'] - self.squashed_table['left']
		return np.sum(lengths)

	def plot_karyotypes(self, chrom_labels=None,
		colors=None, pop_labels=None, title=None):
		"""
		Creates a plot of the ancestry tracts in a pair of chromosomes
		"""
		# Set keyword arguments
		if colors is None:
			prop_cycle = plt.rcParams['axes.prop_cycle']
			colors = prop_cycle.by_key()['color']
		# assert len(colors) == self.num_ancestral_pops

		if pop_labels is None:
			pop_labels = [f'Pop{i}' for i in range(self.num_ancestral_pops)]
		assert len(pop_labels) == self.num_ancestral_pops

		if title is None:
			title = 'Ancestry in admixed individual'

		chrom_labels = {0: 'chr1', 1: 'chr2'}
		length = self._sequence_length

		fig, (chr0, chr1) = plt.subplots(2, figsize=(10,2))
		fig.suptitle(title)
		fig.frameon=False
		fig.legend(
			handles = [Polygon(xy = np.array([[0,0],[0,1],[1,1],[1,0]]), color = i) for i in colors],
			labels = pop_labels,
			loc = 'right'
		)

		for ind, row in self.squashed_table.iterrows():
			if row['sample'] > 1:
				break
			chunk = np.array([[row['left']/length, 0], [row['right']/length, 0],
							  [row['right']/length, 1], [row['left']/length, 1]])
			if chrom_labels[row['sample']] == 'chr1':
				chr0.add_patch(Polygon(xy=chunk, color = colors[int(row['population'])]))
			elif chrom_labels[row['sample']] == 'chr2':
				chr1.add_patch(Polygon(xy=chunk, color = colors[int(row['population'])]))

		chr0.set_ylabel('Chrom 1')
		chr0.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
		# chr1.set_xticks(ticks= [0.25, 0.5, 0.75, 1.0])
		# chr1.set_xticklabels([i*self._sequence_length/4 for i in range(1, 5)])
		chr1.set_xlabel('Chromosomal position (bases)')
		chr1.set_ylabel('Chrom 2')
		chr1.tick_params(left=False, labelleft=False)
		plt.show()

def get_pop_ancestry(ts, census_time):
	"""
	Creates a :class:`tspop.PopAncestry` object from a simulated tree sequence containing
	ancestral census nodes. These are the ancestors that population-based
	ancestry will be calculated with respect to.

	:param tskit.TreeSequence ts: A tree sequence containing census nodes.
	:param census_time: The time at which the census nodes are recorded.
	:type census_time: list(int)
	:returns: a :class:`tspop.PopAncestry` object
	"""

	census_nodes = __get_census_nodes(ts, census_time)
	pop_table = __replace_parents_with_pops(ts, census_nodes)
	return pop_table

def __get_census_nodes(ts, census_time):
	census_nodes = [u.id for u in ts.nodes() if u.time == census_time]
	return census_nodes

def __replace_parents_with_pops(ts, census_nodes):
	ancestor_table = ts.tables.link_ancestors(
		samples=ts.samples(), 
		ancestors=census_nodes
		)
		
	population_ids = ts.tables.nodes.population
	local_ancestry = PopAncestry(left=ancestor_table.left,
		right=ancestor_table.right,
		ancestor=ancestor_table.parent,
		population=[population_ids[n] for n in ancestor_table.parent],
		child=ancestor_table.child,
		sample_nodes=ts.samples(), # May not be in the child field!
		sequence_length=ts.sequence_length
	)

	return local_ancestry

def _plot_ancestry_chunk(row, chrom):
	l = row.left/seq_length
	r = row.right/seq_length
	p = row.population
	if int(p) == 0:
		c = 'blue'
	elif int(p) == 1:
		c = 'red'
	print('p is', p)
	chunk = np.array([[l, 0], [r, 0], [r, 1], [l, 1]])
	chrom.add_patch(Polygon(xy=chunk, color = c))

