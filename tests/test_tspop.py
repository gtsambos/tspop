
import tspop
import msprime

# a test tree sequence.
census_time = 599.5
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
    samples={"SMALL": 0, "BIG": 0, "ADMIX" : 5},
    demography=demography,
    random_seed=1008,
    sequence_length=seq_length,
    recombination_rate=3e-8
)

# Test functions.
# def test_get_census_nodes():
# 	nodes = tspop.get_census_nodes(ts_ex, census_time)
# 	node_table = ts_ex.tables.nodes
# 	for n in nodes:
# 		assert node_table.time[n] == census_time

# def test_replace_parents_with_pops():
# 	census_nodes = tspop.get_census_nodes(ts_ex, census_time)
# 	pop_table = tspop.replace_parents_with_pops(ts_ex, census_nodes)
# 	pops = pop_table['population']
# 	for p in pops:
# 		assert p in [0, 1]

def test_pop_ancestry():
	pop_table = tspop.pop_ancestry(ts_ex, census_time)
	print(pop_table)
