# %%
# BEWARE: The package "concrete" does not support the newest versions of Python
# Please check the requirements in the documentation 
import json
import numpy as np
from concrete import fhe
import numpy as np

net = json.load(open("data/running-example.json"))

# %%
mapping = {}
for n, label in net["transitons"].items():
    if label != '':
        mapping[label] = int(n)
mapping

# %%
matrix = np.matrix(net["matrix"])
enablements = np.matrix(net["enablements"])
pvectors = np.matrix(net["parikh_vectors"])
divisors = enablements.sum(axis=1)
presets = np.matrix(net["presets"])
presets

# %%
# This "cell" implements token replay "in clear". It merges the matrix-oriented
# approach and the usual set-oriented Petri net semantics. You can skip to the
# next "cell"
imarking = [1] + [0]*8

for label in [
        "register request", "check ticket", 
        "examine casually",
        # "decide",
        "reject request"]:
    parikh_vector = [0] * 10
    parikh_vector[mapping[label]] = 1

    req = np.transpose(np.matrix(imarking + parikh_vector))

    selector  = np.matmul(enablements, req) // divisors
    npvector = None
    if (selector.sum() == 1):
        summation = np.zeros(pvectors.shape[1], dtype="int")
        for row, value in zip(pvectors, selector):
            summation = summation + row[0] * value.item(0,0)
        npvector = summation
        imarking = np.matrix(imarking)
    else:
        print("Need to insert tokens")
        preset = np.matrix([0] * len(imarking))
        for row,value in zip(presets, req[9:]):
            preset = preset + row[0] * value.item(0,0)
        imarking = imarking + preset
        npvector = np.matrix(parikh_vector)

    newmarking = imarking.transpose() + np.matmul(matrix, npvector.transpose())
    imarking = newmarking.transpose().tolist()[0]
    print("selector: ", selector.transpose(), summation, imarking)

print(imarking)

# %%
@fhe.compiler({"invector": "encrypted"})
def f(invector):
    selector = np.matmul(enablements, invector) // divisors.transpose()
    parikhv = np.zeros(pvectors.shape[1], dtype="int")
    for row, value in zip(pvectors, selector[0]):
        parikhv = parikhv + row * value

    preset = np.zeros(presets.shape[1], dtype="int")
    for row, value in zip(presets, invector[9:-2]):
        preset = preset + row * value
    
    return np.sum(selector) * (invector[:9] + np.matmul(matrix, parikhv.transpose()).transpose()) + (np.sum(selector) ^ 1) * (invector[:9] + preset + np.matmul(matrix, invector[9:].transpose().transpose())) 

invector_sample = np.random.choice(2, size=(100,19))
circuit = f.compile(invector_sample)

imarking = [1] + [0]*8
print("Initial marking: ", imarking)
# You can comment out one or several labels to force token adition
for label in [
        "register request", 
        "check ticket", 
        "examine casually",
        # "decide",
        "reject request"]:
    parikh_vector = [0] * 10
    parikh_vector[mapping[label]] = 1

    request = imarking + parikh_vector
    print("request: ", request)
    imarking = circuit.encrypt_run_decrypt(request)[0].tolist()
    print("new marking: ", imarking)

# %%
