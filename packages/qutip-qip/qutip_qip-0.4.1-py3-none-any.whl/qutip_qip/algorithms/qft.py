"""
This module provides the circuit implementation for Quantum Fourier Transform.
"""

import numpy as np
from ..operations import Gate, snot, cphase, swap, expand_operator
from ..circuit import QubitCircuit
from qutip import Qobj
from ..decompose import decompose_one_qubit_gate


__all__ = ["qft", "qft_steps", "qft_gate_sequence"]


def qft(N=1):
    """
    Quantum Fourier Transform operator on N qubits.

    Parameters
    ----------
    N : int
        Number of qubits.

    Returns
    -------
    QFT: qobj
        Quantum Fourier transform operator.

    """
    if N < 1:
        raise ValueError("Minimum value of N can be 1")

    N2 = 2**N
    phase = 2.0j * np.pi / N2
    arr = np.arange(N2)
    L, M = np.meshgrid(arr, arr)
    L = phase * (L * M)
    L = np.exp(L)
    dims = [[2] * N, [2] * N]
    return Qobj(1.0 / np.sqrt(N2) * L, dims=dims)


def qft_steps(N=1, swapping=True):
    """
    Quantum Fourier Transform operator on N qubits returning the individual
    steps as unitary matrices operating from left to right.

    Parameters
    ----------
    N: int
        Number of qubits.
    swap: boolean
        Flag indicating sequence of swap gates to be applied at the end or not.

    Returns
    -------
    U_step_list: list of qobj
        List of Hadamard and controlled rotation gates implementing QFT.

    """
    if N < 1:
        raise ValueError("Minimum value of N can be 1")

    U_step_list = []
    if N == 1:
        U_step_list.append(snot())
    else:
        for i in range(N):
            for j in range(i):
                U_step_list.append(
                    expand_operator(
                        cphase(np.pi / (2 ** (i - j))),
                        dims=[2] * N,
                        targets=[i, j],
                    )
                )
            U_step_list.append(
                expand_operator(snot(), dims=[2] * N, targets=i)
            )
        if swapping:
            for i in range(N // 2):
                U_step_list.append(
                    expand_operator(
                        swap(), dims=[2] * N, targets=[N - i - 1, i]
                    )
                )
    return U_step_list


def qft_gate_sequence(N=1, swapping=True, to_cnot=False):
    """
    Quantum Fourier Transform operator on N qubits returning the gate sequence.

    Parameters
    ----------
    N: int
        Number of qubits.
    swap: boolean
        Flag indicating sequence of swap gates to be applied at the end or not.

    Returns
    -------
    qc: instance of QubitCircuit
        Gate sequence of Hadamard and controlled rotation gates implementing
        QFT.
    """

    if N < 1:
        raise ValueError("Minimum value of N can be 1")

    qc = QubitCircuit(N)
    if N == 1:
        qc.add_gate("SNOT", targets=[0])
    else:
        for i in range(N):
            for j in range(i):
                if not to_cnot:
                    qc.add_gate(
                        "CPHASE",
                        targets=[j],
                        controls=[i],
                        arg_label=r"{\pi/2^{%d}}" % (i - j),
                        arg_value=np.pi / (2 ** (i - j)),
                    )
                else:
                    decomposed_gates = _cphase_to_cnot(
                        [j], [i], np.pi / (2 ** (i - j))
                    )
                    qc.gates.extend(decomposed_gates)
            qc.add_gate("SNOT", targets=[i])
        if swapping:
            for i in range(N // 2):
                qc.add_gate("SWAP", targets=[N - i - 1, i])
    return qc


def _cphase_to_cnot(targets, controls, arg_value):
    rotation = Qobj([[1.0, 0.0], [0.0, np.exp(1.0j * arg_value)]])
    decomposed_gates = list(
        decompose_one_qubit_gate(rotation, method="ZYZ_PauliX")
    )
    new_gates = []
    gate = decomposed_gates[0]
    gate.targets = targets
    new_gates.append(gate)
    new_gates.append(Gate("CNOT", targets=targets, controls=controls))
    gate = decomposed_gates[4]
    gate.targets = targets
    new_gates.append(gate)
    new_gates.append(Gate("CNOT", targets=targets, controls=controls))
    new_gates.append(Gate("RZ", targets=controls, arg_value=arg_value / 2))
    gate = decomposed_gates[7]
    gate.arg_value += arg_value / 4
    new_gates.append(gate)
    return new_gates
