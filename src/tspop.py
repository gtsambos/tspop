
import tskit
import pandas as pd

def pop_ancestry(ts, census_time):
	census_nodes = _get_census_nodes(ts, census_time)
	pop_table = _replace_parents_with_pops(ts, census_nodes)
	pop_table = _squash_ancestry_tracts(pop_table)
	pop_table = pop_table[['child', 'population', 'left', 'right']]
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
	local_ancestry = pd.DataFrame(
	    data = {
	        'left': ancestor_table.left,
	        'right': ancestor_table.right,
	        'population' : [population_ids[n] for n in ancestor_table.parent],
	        'child' : ancestor_table.child
	    })
	return local_ancestry

def _squash_ancestry_tracts(local_ancestry):
	new_sample = []
	new_left = []
	new_right = []
	new_population = []

	local_ancestry.sort_values(
	    by=['child','left'], inplace=True, ignore_index=True)

	for ind, row in local_ancestry.iterrows():
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


