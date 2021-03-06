
import tspop
import msprime
import pytest

# a test tree sequence.
census_time = 20.5
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
	time=20,
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
	samples={"SMALL": 0, "BIG": 0, "ADMIX" : 2},
	demography=demography,
	random_seed=1008,
	sequence_length=seq_length,
	recombination_rate=3e-8
)

def test_ancestry_table():
	t = tspop.PopAncestry(
		left=[], right=[], population=[], ancestor=[], child=[],
		sample_nodes=[], sequence_length=1)

def test_ancestry_table_bad_input():
	with pytest.raises(Exception):
		tspop.PopAncestry(
			left=[0], right=[], population=[], ancestor=[], child=[])

def test_pop_ancestry():
	p = tspop.get_pop_ancestry(ts_ex, census_time)
	print("PopAncestry summary info:")
	print(p)

def test_table_output():
	pop_table = tspop.get_pop_ancestry(ts_ex, census_time)
	print("Table output:")
	print(pop_table.squashed_table)
	print(pop_table.ancestry_table)

def test_calculate_global_ancestry():
	pop_table = tspop.get_pop_ancestry(ts_ex, census_time)
	st = pop_table.squashed_table
	st0 = st[st.population == 0]
	print(st0)
	pop0_lengths = sum(st0.right - st0.left)
	print(pop0_lengths/pop_table.total_genome_length)


