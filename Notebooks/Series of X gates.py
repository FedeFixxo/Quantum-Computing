from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt
from time import time


def getCircuitCounts(qc: QuantumCircuit, noisy=True, shots = 1024):
    backend = FakeManilaV2() if noisy else AerSimulator()

    retDict = SamplerV2(backend).run([
        generate_preset_pass_manager(backend=backend, optimization_level=0)
            .run(qc)
    ], shots=shots).result()[0].data.out.get_counts()

    return { k:retDict[k] for k in sorted(retDict) }


def getQC_n(nX = 0):
    qReg = QuantumRegister(1, 'Qubit')
    cReg = ClassicalRegister(1, 'out')
    qc = QuantumCircuit(qReg, cReg)
    
    for i in range(nX):
        qc.x(qReg)

    qc.measure(qReg, cReg)
    return qc


def main():
    depth = 10
    bunchSize = 3
    shots = 100

    print(f'Running {depth} circuits...')

    data = {}
    startTime = time()
    for n in range(depth):
        if n % bunchSize == 0:
            if n != 0:
                print(f'{(time() - startTime):.3f} s')
            print(f"#{n:>4d}-{ min(depth, n+bunchSize)-1 :<4d}:", end="\t", flush=True)
            startTime = time()

        counts = getCircuitCounts(getQC_n(n), shots=shots)
        data[n] = counts[f'{n%2}'] / shots

        # Statistics about each iteration, they may slow things down
        # print(f'\t\tCorrect rate: {correctCounts}/{counts["0"] + counts["1"]}', end='\n\n')
    
    print(f'{(time() - startTime):.3f} s')
    plt.plot(data.values())
    plt.title("Fraction of correct results")
    plt.show()

if __name__ == '__main__':
    main()