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

    summation = 0
    with open(file_name, 'r') as file:
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
        
            imarking = newmarking.transpose().tolist()[0]
        
        print(imarking)
        
        end_time = time.time()
        print(file_name, ":", index, " - Execution time: ", end_time - init_time)
