from math import log2
from qiskit import Aer, execute, transpile
import warnings
warnings.filterwarnings('ignore')
from qiskit.test.mock import FakeProvider
from qiskit.providers.aer.noise import NoiseModel
import numpy as np
import random

def runOnSimulator(circuits):
    print("Running on simulator to get ground truth")
    simulator = Aer.get_backend('statevector_simulator')
    res = []
    for circuit in circuits:
        job = execute(circuit, simulator)
        result = job.result()
        stv = result.get_statevector(circuit, decimals=3)
        probs = stv.probabilities()
        bestIdxs = np.argwhere(probs == np.amax(probs)).flatten().tolist()
        n = (int)(log2(len(probs)))
        getbinary = lambda x, n: format(x, 'b').zfill(n)
        bestIdxsBin = [getbinary(i, n) for i in bestIdxs]
        res.append(bestIdxsBin)
    return res



def runOnBackend(backend, circuit):
    simulator = Aer.get_backend('qasm_simulator')
    noise_model = NoiseModel.from_backend(backend, warnings=False)

    # Execute the circuit on the simulator with error characteristics of the given backend
    job = execute(circuit, simulator, shots=1024, noise_model=noise_model)

    # Grab results from the job
    result = job.result()
    return result.get_counts()


def tryBackends(circuits):
    print("Running backend experiment batch")
    provider = FakeProvider()
    backends = [ b.name() for b in provider.backends() if b.configuration().n_qubits >= 10] 
    counts = [{} for _ in range(len(circuits)*len(backends))] 
    for i in range(len(backends)):
        be = provider.get_backend(backends[i])
        counts[i::len(backends)] = runOnBackend(be, circuits)

    return counts


def tryOptimizations(backend, circuits):
    print("Creating optimization experiment job")
    transpiledCircuits = []
    for circuit in circuits:
        for i in range(4):
            transpiledCircuits.append(transpile(circuit, backend=backend, optimization_level=i, seed_transpiler=123))

    job = execute(transpiledCircuits, backend, shots=4096)

    return job

def runOnSimulator(circuits):
    print("Running on simulator to get ground truth")
    simulator = Aer.get_backend('statevector_simulator')
    res = []
    for circuit in circuits:
        job = execute(circuit, simulator)
        result = job.result()
        stv = result.get_statevector(circuit, decimals=3)
        probs = stv.probabilities()
        bestIdxs = np.argwhere(probs == np.amax(probs)).flatten().tolist()
        n = (int)(log2(len(probs)))
        getbinary = lambda x, n: format(x, 'b').zfill(n)
        bestIdxsBin = [getbinary(i, n) for i in bestIdxs]
        res.append(bestIdxsBin)
    return res

def tryTranspilations(backend, circuits, N=9):
    print("Creating transpilation seed experiment job")
    transpiledCircuits = []
    for circuit in circuits:
        for i in range(N):
            transpiledCircuits.append(transpile(circuit, backend=backend, seed_transpiler=random.randrange(0, 10000)))

    job = execute(transpiledCircuits, backend, shots=4096)

    return job