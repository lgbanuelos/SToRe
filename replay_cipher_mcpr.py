import json
import numpy as np
import numpy as np
from   concrete import fhe
import time
import sys

runs = 1
init_time = time.time()

net = json.load(open("data/running-example.json"))

mapping = {}
for n, label in net["transitons"].items():
    if label != '':
        mapping[label] = int(n)
mapping

matrix = np.matrix(net["matrix"])
enablements = np.matrix(net["enablements"])
pvectors = np.matrix(net["parikh_vectors"])
divisors = enablements.sum(axis=1)
presets = np.matrix(net["presets"])
presets

@fhe.compiler({"invector": "encrypted"})
def f(invector):

    fmarking = [0]*8 + [1]
    imarking = invector[:9]

    invectorp = np.fmin(invector, np.ones(len(invector), dtype=int))
    selector = np.matmul(enablements, invectorp) // divisors.transpose()

    parikhv = np.zeros(pvectors.shape[1], dtype="int")
    for row, value in zip(pvectors, selector[0]):
        parikhv = parikhv + row * value

    preset = np.zeros(presets.shape[1], dtype="int")
    for row, value in zip(presets, invector[9:-2]):
        preset = preset + row * value

    newmarking = np.sum(selector) * (invector[:9] + np.matmul(matrix, parikhv.transpose()).transpose()) + (np.sum(selector) ^ 1) * (invector[:9] + preset + np.matmul(matrix, invector[9:].transpose().transpose())) 

    #Computing c, m, p, r
    #---------------------------------------- m
    zeros = np.zeros(imarking.shape, dtype="int")
    subsin = np.subtract( imarking, newmarking)
    maxs = np.fmax(subsin, zeros)

    #---------------------------------------- m
    m    = np.sum(preset) * (1 - np.sum(selector))

    #---------------------------------------- c
    c    = np.sum( np.array(maxs) ) + m

    #---------------------------------------- p
    subsni = np.subtract( newmarking, imarking)
    maxsni = np.fmax(subsni, zeros)
    p      = np.sum( np.array(maxsni) ) - m

    #---------------------------------------- r
    subsnf = np.subtract(newmarking, fmarking)
    sumsnf = np.sum(subsnf)
    unos   = np.ones(imarking.shape, dtype="int")
    minnon = np.fmin(newmarking, unos)
    fxmon  = np.multiply( fmarking, minnon )
    sumf   = np.sum(fmarking)
    divr   = fxmon // sumf
    sums   = np.sum(divr)
    r      = sumsnf * sums

    return newmarking, m, c, p, r


for index in range(1,runs + 1):
    print("******************************************************* Execution: ", index)

    file_name = sys.argv[1]

    ############################### fhe compile
    init_time = time.time()

    invector_sample = np.random.choice(4, size=(100,19))
    circuit = f.compile(invector_sample)

    end_time = time.time()
    print(file_name, ":", index, " - fhe compile time: ", end_time - init_time)
    ############################### end fhe compile

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
        
            request = imarking + parikh_vector
            print("request: ", request)
            result = circuit.encrypt_run_decrypt(request)
            imarking = result[0][0].tolist()
            m, c, p, r = result[1:]
            print("result: ", result)
            print("new marking: ", imarking)
            print("m:", m, " c:", c , " p:", p, " r:", r)
            print("==================================================")
        
            mf = mf + m
            cf = cf + c
            pf = pf + p
            rf = rf + r

        fitness = 0.5 * (1 -(mf/cf)) + 0.5*(1-(rf/pf))

        print("mf:", mf, " cf:", cf , " pf:", pf, " rf:", rf)
        print("fitness: ", fitness)

        end_time = time.time()
        print(index, "- Execution time: ", end_time - init_time)
