
import tspop
import msprime

def test_num_pops():
	ts = msprime.sim_ancestry(2)
	tspop.num_pops(ts)