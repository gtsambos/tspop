
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

	def __init__(self, left, right, population, ancestor, child):
		self.left = np.array(left, dtype=np.float64)
		self.right = np.array(right, dtype=np.float64)
		self.population = np.array(population, dtype=np.int32)
		self.ancestor = np.array(ancestor, dtype=np.int32)
		self.child = np.array(child, dtype=np.int32)
		self.num_rows = self.num_rows()
		# Create the ancestry tables
		self.ancestry_table = pd.DataFrame(
		data = {
			'left': left,
			'right': right,
			'ancestor' : ancestor,
			'population' : population,
			'child' : child
		})
		self.ancestry_table.sort_values(
			by=['child','left'], inplace=True, ignore_index=True)
		# Squashed table
		self.squashed_table = self.squash_ancestry_tracts()
		self.squashed_table = self.squashed_table[['child', 'population', 'left', 'right']]
		# Raw table
		self.ancestry_table = self.ancestry_table[['child', 'population', 'ancestor', 'left', 'right']]

	def __str__(self):
		ret = "id\tleft\t\tright\t\tancestor\t\tpopulation\tchild\n"
		for j in range(self.num_rows):
			ret += "{}\t{:.8f}\t{:.8f}\t{}\t{}\t{}\n".format(
				j, self.left[j], self.right[j], self.ancestor[j], self.population[j], self.child[j])
		return ret[:-1]

	def num_rows(self):
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
		assert len(self.population) == len(self.child)

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
			if ind > 0 and row['left']==new_right[-1] and row['population'] == new_population[-1] and row['child'] == new_sample[-1]:
				new_right[-1] = row['right']
			else:
				new_sample.append(row['child'])
				new_left.append(row['left'])
				new_right.append(row['right'])
				new_population.append(row['population'])
				
		squashed_ancestry_table = pd.DataFrame({
			'child': [int(i) for i in new_sample],
			'left' : new_left,
			'right': new_right,
			'population' : [int(p) for p in new_population]
		})

		return(squashed_ancestry_table)

def pop_ancestry(ts, census_time):
	"""
	Creates a PopAncestry object.
	:param tskit.TreeSequence ts: A tree sequence containing census nodes.
	:param census_time: The time at which the census nodes are recorded.
	:type census_time: list(int)
	"""
	census_nodes = _get_census_nodes(ts, census_time)
	pop_table = _replace_parents_with_pops(ts, census_nodes)
	return pop_table

def _get_census_nodes(ts, census_time):
	census_nodes = [u.id for u in ts.nodes() if u.time == census_time]
	return census_nodes

def _replace_parents_with_pops(ts, census_nodes):
	ancestor_table = ts.tables.link_ancestors(
		samples=ts.samples(), 
		ancestors=census_nodes
		)
	population_ids = ts.tables.nodes.population
	local_ancestry = PopAncestry(left=ancestor_table.left,
		right=ancestor_table.right,
		ancestor=ancestor_table.parent,
		population=[population_ids[n] for n in ancestor_table.parent],
		child=ancestor_table.child
	)

	return local_ancestry

