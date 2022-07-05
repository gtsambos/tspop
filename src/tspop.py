
import tskit
import pandas as pd
import numpy as np

class PopAncestry(object):
	"""
	A table showing all genomic segments of the specified sample IDs
	that have ancestry with one of the specified populations.
	Each row (L, R, P, S) indicates that over the genomic interval
	with coordinates (L, R), the sample node with ID S has inherited
	from an ancestral node in population P.
	:ivar left: The array of left coordinates.
	:vartype left: numpy.ndarray, dtype=np.float64
	:ivar right: The array of right coordinates.
	:vartype right: numpy.ndarray, dtype=np.float64
	:ivar population: The array of population labels.
	:vartype population: numpy.ndarray, dtype=np.int32
	"""

	def __init__(self, left, right, population, ancestor, child,
		sample_nodes, sequence_length):
		self.left = np.array(left, dtype=np.float64)
		self.right = np.array(right, dtype=np.float64)
		self.population = np.array(population, dtype=np.int32)
		self.ancestor = np.array(ancestor, dtype=np.int32)
		self.sample = np.array(child, dtype=np.int32)
		self.num_rows = self.__num_rows()
		
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
		self.squashed_table = self.squash_ancestry_tracts()
		# Reorder the raw table
		self.ancestry_table = self.ancestry_table[['sample', 'left', 'right', 'ancestor', 'population']]

		# Summary attributes. Some are just wrappers for the ts attributes -- needed?
		self.ancestral_pops = list(set(self.squashed_table['population']))
		self.num_ancestral_pops = len(self.ancestral_pops)
		self.samples = sample_nodes
		self.num_samples = len(sample_nodes)
		self.ancestors = list(set(self.ancestry_table['ancestor']))
		self.num_ancestors = len(self.ancestors)
		self.total_genome_length = sequence_length * self.num_samples
		self.coverage = self.calculate_coverage()

	def __str__(self):
		ret = """\n\nPopAncestry summary\n\n"""
		ret += "Number of ancestral populations: \t{}\n".format(self.num_ancestral_pops)
		ret += "Number of sample chromosomes: \t\t{}\n".format(self.num_samples)
		ret += "Number of ancestors: \t\t\t{}\n".format(self.num_ancestors)
		ret += "Total length of genomes: \t\t{:.6f}\n".format(self.total_genome_length)
		ret += "Ancestral coverage: \t\t\t{:.6f}\n".format(self.coverage)
		return ret[:-1]

	def __num_rows(self):
		"""
		Returns the number of rows in the table.
		"""
		self.check_row_lengths()
		return len(self.left)

	def check_row_lengths(self):
		"""
		Checks that the length of each input field is the same.
		"""
		assert len(self.left) == len(self.right)
		assert len(self.right) == len(self.population)
		assert len(self.population) == len(self.sample)

	def squash_ancestry_tracts(self):
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

	def calculate_coverage(self):
		lengths = self.squashed_table['right'] - self.squashed_table['left']
		return np.sum(lengths)

def pop_ancestry(ts, census_time):
	"""
	Creates a PopAncestry object.
	:param tskit.TreeSequence ts: A tree sequence containing census nodes.
	:param census_time: The time at which the census nodes are recorded.
	:type census_time: list(int)
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

