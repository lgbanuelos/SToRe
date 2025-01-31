# Please check the requirements in the documentation (python version, testing on 3.10)
import json
import numpy as np
import time
import sys

runs = 1
net = json.load(open("data/running-example.json"))

mapping = {}
for n, label in net["transitons"].items():
    if label != '':
        mapping[label] = int(n)
print(mapping)

matrix = np.matrix(net["matrix"])
enablements = np.matrix(net["enablements"])
pvectors = np.matrix(net["parikh_vectors"])
divisors = enablements.sum(axis=1)
presets = np.matrix(net["presets"])
presets

# %%
# This "cell" implements token replay "in clear". It merges the matrix-oriented
# approach and the usual set-oriented Petri net semantics. 

for index in range(1,runs+1):
    print("******************************************************* Execution: ", index)

    file_name = sys.argv[1]
    init_time = time.time()
    
    imarking = [1] + [0]*8
    fmarking = [0]*8 + [1]
    print("Initial marking: ", imarking)
    print("final marking: ", fmarking)
    print("==================================================: " + file_name);

    with open(file_name, 'r') as file:

        mf = 0
        cf = 0
        pf = 0
        rf = 0

        for label in file:
            print(label.strip())
            parikh_vector = [0] * 10
            parikh_vector[mapping[label.strip()]] = 1
        
            imarking_o = imarking   #imarking original
            imarking_h = np.fmin(imarking, np.ones(len(imarking), dtype=int))
        
            imh_pv = np.concatenate( (imarking_h, parikh_vector) )
            req = np.transpose(np.matrix(imh_pv))
            selector  = np.matmul(enablements, req) // divisors
        
            preset = np.matrix([0] * len(imarking))
            npvector = None
            summation = 0
            if (selector.sum() == 1):
                summation = np.zeros(pvectors.shape[1], dtype="int")
                for row, value in zip(pvectors, selector):
                    summation = summation + row[0] * value.item(0,0)
                npvector = summation
                imarking = np.matrix(imarking)
            else:
                print("Need to insert tokens")
                # preset = np.matrix([0] * len(imarking)) ** moved outside the if
                for row,value in zip(presets, req[9:]):
                    preset = preset + row[0] * value.item(0,0)
                imarking = imarking + preset
                npvector = np.matrix(parikh_vector)
        
            newmarking = imarking.transpose() + np.matmul(matrix, npvector.transpose())
            print("selector: ", selector.transpose(), summation, imarking)
        
            #Computing c, m, p, r
            
            # print("-------------------- m")
            m    = preset.sum() * (1 - selector.sum())
        
            # print("preset: ", preset)
            # print("m: ", m)
        
            # print("-------------------- c")
            zeros = np.zeros(imarking.shape, dtype="int")
            subsin = imarking_o - newmarking.transpose()
            maxs = np.fmax(subsin, zeros)
            c    = np.sum( np.array(maxs) ) + m
        
            # print("imarking   : ", imarking_o)
            # print("newmarking : ", newmarking.transpose())
            # print("subs i-n     : ", subsin)
            # print("zeros        : ", zeros)
            # print("maxs (i-n, 0): ", maxs)
            # print("c: ", c)
            # print("-------------------- p")
        
            subsni = newmarking.transpose() - imarking_o
            maxsni =  np.fmax(subsni, zeros)
            p    = np.sum( np.array(maxsni) ) - m
        
            # print("subs n-i     : ", subsni)
            # print("maxs (n-i, 0): ", maxsni)
            # print("p: ", p)
        
            # print("-------------------- r")
            subsnf = np.subtract(newmarking.transpose(), fmarking)
            sumsnf = np.sum(subsnf)
            unos = np.ones(imarking.shape, dtype="int")
            minnon = np.fmin(np.array(newmarking.transpose()), np.array(unos))
            fxmon  = np.multiply( fmarking, minnon )
            sumf   = np.sum(fmarking)
            divr   = fxmon // sumf
            sums   = np.sum(divr)
            r      = sumsnf * sums
        
            # print("newmarking: ", newmarking.transpose())
            # print("unos: ", unos)
            # print("subsnf: ", subsnf)
            # print("sumsnf: ", subsnf)
            # print("minnon: ", minnon)
            # print("fxmon: ", minnon)
            # print("sumf: ", sumf)
            # print("divr: ", divr)
            # print("sums: ", sums)
            # print("r: ", r)
        
            print("m:", m, " c:", c , " p:", p, " r:", r)
            print("==================================================")

            mf = mf + m
            cf = cf + c
            pf = pf + p
            rf = rf + r
        
            imarking = newmarking.transpose().tolist()[0]
        print(imarking)

        fitness = 0.5 * (1 -(mf/cf)) + 0.5*(1-(rf/pf))

        print("mf:", mf, " cf:", cf , " pf:", pf, " rf:", rf)
        print("fitness: ", fitness)

        
        end_time = time.time()
        print(file_name, ":", index, " - Execution time: ", end_time - init_time)
