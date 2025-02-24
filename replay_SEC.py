import json
import numpy as np
import numpy as np
from   concrete import fhe
import time
import sys

runs = 1

net = json.load(open("data/BPI_challenge_2012/bpi_challenge_2012.json"))

mapping = {}
for n, label in net["transitons"].items():
    if label != '':
        mapping[label] = int(n)
print(mapping)

matrix = np.matrix(net["matrix"])
enablements = np.matrix(net["enablements"])
firing = np.matrix(net["firing"])
pvectors = np.matrix(net["parikh_vectors"])
divisors = enablements.sum(axis=1)
presets = np.matrix(net["presets"])

print("matrix: \n", matrix)
print("enablements: \n", enablements)
print("firing: \n", firing)
print("pvectors: \n", pvectors)
print("divisors: \n", np.transpose(divisors))
print("presets: \n", presets)

@fhe.compiler({"invector": "encrypted"})
def f(invector):

    fmarking = [0]*9 + [1]
    imarking = invector[:10]

    invectorp = np.fmin(invector, np.ones(len(invector), dtype=int))
    selector = np.matmul(enablements, invectorp) // divisors.transpose()

    parikhv = np.zeros(pvectors.shape[1], dtype="int")
    for row, value in zip(pvectors, selector[0]):
        parikhv = parikhv + row * value

    preset = np.zeros(presets.shape[1], dtype="int")
    for row, value in zip(presets, invector[10:]):
        preset = preset + row * value

    newmarking = np.sum(selector) * (invector[:10] + np.matmul(matrix, parikhv.transpose()).transpose())
            # + (np.sum(selector) ^ 1) * (invector[:10] + preset + np.matmul(matrix, invector[10:].transpose().transpose())) 
            #TODO: check error, matrix size = 11, invector[10:] size = 8 (parikh vector).

    return newmarking


for index in range(1,runs + 1):
    print("******************************************************* Execution: ", index)

    file_name = sys.argv[1]

    ############################### fhe compile
    init_time = time.time()

    invector_sample = np.random.choice(4, size=(100,18))
    circuit = f.compile(invector_sample)

    end_time = time.time()
    print(file_name, ":", index, " - fhe compile time: ", end_time - init_time)
    ############################### end fhe compile

    init_time = time.time()
    
    imarking = [1] + [0]*9
    fmarking = [0]*9 + [1]
    print("Initial marking: ", imarking)
    print("final marking: ", fmarking)
    print("==================================================: " + file_name);

    with open(file_name, 'r') as file:
        for label in file:
            print(label.strip())
            parikh_vector = [0] * 8
            parikh_vector[mapping[label.strip()]] = 1
        
            request = imarking + parikh_vector
            print("request: ", request)
            imarking = circuit.encrypt_run_decrypt(request)[0].tolist()
            print("new marking: ", imarking)
            print("==================================================")
        
        end_time = time.time()
        print(index, "Execution time: ", end_time - init_time)
