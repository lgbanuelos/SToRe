#!/bin/python3

import pm4py
#from pm4py.algo.decision_mining import algorithm as dem

pn, im, fm = pm4py.read_pnml('./1.models/Model_O.pnml')
pm4py. view_petri_net(pn, im, fm, format='svg')

matrix = pm4py.algo.analysis.woflan.graphs.utility.compute_incidence_matrix(pn)

print(matrix)
