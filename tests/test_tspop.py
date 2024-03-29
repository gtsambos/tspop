
import tspop
import msprime
import tskit
import pytest
import pandas as pd
import io

# a test tree sequence.
def sim_ts():
	census_time = 201
	demography = msprime.Demography()
	demography.add_population(
		name="SMALL", initial_size=200)
	demography.add_population(
		name="BIG", initial_size=500)
	demography.add_population(
		name="ADMIX", initial_size=200)
	demography.add_population(
		name="ANC", initial_size=500)
	demography.add_admixture(
		time=200,
		derived="ADMIX",
		ancestral=["SMALL", "BIG"],
		proportions=[0.5, 0.5]
	)
	demography.add_census(time=census_time)
	demography.add_population_split(
		time=600,
		derived=["SMALL", "BIG"],
		ancestral="ANC"
	)
	seq_length = 1e7
	ts_ex = msprime.sim_ancestry(
		samples={"SMALL": 0, "BIG": 0, "ADMIX" : 20},
		demography=demography,
		random_seed=1008,
		sequence_length=seq_length,
		recombination_rate=3e-8
	)

	return (ts_ex, census_time)

class TestBasicUsage():
	"""Tests the table output."""

	(ts_ex, census_time) = sim_ts()
	p = tspop.get_pop_ancestry(ts_ex, census_time)

	def test_ancestry_table(self):
		t = tspop.PopAncestry(
			left=[], right=[], population=[], ancestor=[], child=[],
			sample_nodes=[], sequence_length=1)

	def test_ancestry_table_bad_input(self):
		with pytest.raises(Exception):
			tspop.PopAncestry(
				left=[0], right=[], population=[], ancestor=[], child=[])

	def test_pop_ancestry(self):
		print("PopAncestry summary info:")
		print(self.p)

	def test_table_output(self):
		print("Table output:")
		print(self.p.squashed_table)
		print(self.p.ancestry_table)

	def test_calculate_global_ancestry(self):
		st = self.p.squashed_table
		st0 = st[st.population == 0]
		# print(st0)
		pop0_lengths = sum(st0.right - st0.left)
		print(pop0_lengths/self.p.total_genome_length)

	def test_ancestry_fraction(self):
		p0 = self.p.calculate_ancestry_fraction(population=0)
		p1 = self.p.calculate_ancestry_fraction(population=1)
		assert pytest.approx(p0 + p1) == 1

	def test_ancestry_fraction_sample(self):
		p0 = self.p.calculate_ancestry_fraction(population=0, sample=2)
		p1 = self.p.calculate_ancestry_fraction(population=1, sample=2)
		assert pytest.approx(p0 + p1) == 1

	def test_ancestry_fraction_errors(self):
		with pytest.raises(ValueError):
			self.p.calculate_ancestry_fraction(population=4)
		with pytest.raises(ValueError):
			self.p.calculate_ancestry_fraction(population=0, sample=40)

	def test_subset_tables(self):
		a, s = self.p.subset_tables(subset_samples=[0, 1])
		assert len(set(a['sample'])) == 2
		assert len(set(s['sample'])) == 2
	

class TestPlots:
	"""Tests karyotype plotting."""

	(ts_ex, census_time) = sim_ts()

	def test_karyotype(self):
		pop_table = tspop.get_pop_ancestry(self.ts_ex, self.census_time)
		pop_table.plot_karyotypes(
			sample_pair= [0,3],
			title="Hominin ancestry in an Homo Sapiens individual",
			length_in_Mb=True,
			pop_labels=['HomSap', 'HomNea', 'ArcAfr'],
			height=4,
			width=13,
			# outfile="myfile.png",
			)

class TestIbdSquash:
	"""Tests the method for squashing the IBD segments obtained from
	tskit.ibd_segments(). (ie. calculates ibd in a 'path-agnostic' way.)"""

	def test_basic(self):
		#
		#        4       |      4       |        4
		#       / \      |     / \      |       / \
		#      /   \     |    /   3     |      /   \
		#     /     \    |   2     \    |     /     \
		#    /       \   |  /       \   |    /       \
		#   0         1  | 0         1  |   0         1
		#                |              |
		#                1.0            2.0            3.0
		nodes = io.StringIO(
			"""\
		id	is_sample	time
		0	1			0
		1	1			0
		2	0			0.5
		3	0			0.8
		4	0			1		
		"""
		)
		edges = io.StringIO(
			"""\
		left	right	parent	child
		1.0		2.0		2		0
		1.0		2.0		3		1
		0.0		1.0		4		0
		0.0		1.0		4		1
		2.0		3.0		4		0
		2.0		3.0		4		1
		1.0		2.0		4		2
		1.0		2.0		4		3
		"""
		)
		ts = tskit.load_text(nodes=nodes, edges=edges, strict=False)
		res = ts.ibd_segments(store_segments=True)
		ress = tspop._path_agnostic_ibd(res)
		
		# Test output is as expected.
		assert len(ress.keys()) == 1
		assert isinstance(ress[(0, 1)], pd.DataFrame)
		ans = pd.DataFrame({
			'left' : [0.0],
			'right' : [3.0],
			'ancestor' : [4]
		})
		ans = ans.astype({
			'left' : float,
			'right' : float,
			'ancestor' : int
			})
		pd.testing.assert_frame_equal(ress[(0, 1)], ans)

	def test_dont_oversquash(self):
		#                |              |         5
		#        4       |      4       |        / 4
		#       / \      |     / \      |       /   \
		#      /   \     |    /   \     |      /     3
		#     /     \    |   2     \    |     /       \
		#    /       \   |  /       \   |    /         \
		#   0         1  | 0         1  |   0           1
		#                |              |
		#                1.0            2.0             3.0
		nodes = io.StringIO(
			"""\
		id	is_sample	time
		0	1			0
		1	1			0
		2	0			0.5
		3	0			0.8
		4	0			1
		5	0			1.3		
		"""
		)
		edges = io.StringIO(
			"""\
		left	right	parent	child
		1.0		2.0		2		0
		2.0		3.0		3		1
		0.0		1.0		4		0
		0.0		2.0		4		1
		1.0		2.0		4		2
		2.0		3.0		4		3
		2.0		3.0		5		0
		2.0		3.0		5		4
		"""
		)
		ts = tskit.load_text(nodes=nodes, edges=edges, strict=False)
		res = ts.ibd_segments(store_segments=True)
		ress = tspop._path_agnostic_ibd(res)

		# Test output is as expected.
		assert len(ress.keys()) == 1
		assert isinstance(ress[(0, 1)], pd.DataFrame)
		ans = pd.DataFrame({
			'left' : [0.0, 2.0],
			'right' : [2.0, 3.0],
			'ancestor' : [4, 5]
		})
		ans = ans.astype({
			'left' : float,
			'right' : float,
			'ancestor' : int
			})
		pd.testing.assert_frame_equal(ress[(0, 1)], ans)

