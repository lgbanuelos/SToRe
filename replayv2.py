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

@fhe.compiler({"invector": "encrypted"})
def f(invector):
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
    zeros = np.zeros(imarking.shape, dtype="int")
    subsin = np.subtract( imarking, newmarking)
    maxs = np.fmax(subsin, zeros)

    m    = np.sum(preset) * (1 - np.sum(selector))
    c    = np.sum( np.array(maxs) ) + m

    subsni = np.subtract( newmarking, imarking)
    maxsni = np.fmax(subsni, zeros)
    p      = np.sum( np.array(maxsni) ) - m

    # return newmarking, subsin, maxs, c, m, p
    return newmarking, imarking, newmarking, subsin, zeros, maxs, c

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
    result = circuit.encrypt_run_decrypt(request)
    imarking = result[0][0].tolist()
    print("result: ", result)
    print("new marking: ", imarking)

# %%
