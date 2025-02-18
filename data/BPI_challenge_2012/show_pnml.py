import pm4py
#from pm4py.algo.decision_mining import algorithm as dem

pn, im, fm = pm4py.read_pnml('./1.models/Model_O.pnml')
pm4py. view_petri_net(pn, im, fm, format='svg')
