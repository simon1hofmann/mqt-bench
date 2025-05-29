# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""HRS Cumulative Multiplier."""

from __future__ import annotations

from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.arithmetic import HalfAdderGate, ModularAdderGate


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Create a hrs cumulative multiplier circuit.

    Arguments:
            num_qubits: Number of qubits of the returned quantum circuit, must be divisible by 4.

    Returns:
           QuantumCircuit: The constructed hrs cumulative multiplier circuit.
    """
    if num_qubits % 4 or num_qubits < 4:
        msg = "num_qubits must be ≥ 4 and divisible by 4."
        raise ValueError(msg)

    num_state_qubits = num_qubits // 4
    num_result_qubits = 2 * num_state_qubits

    # define the registers
    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits, name="b")
    qr_out = QuantumRegister(num_result_qubits, name="out")

    qc = QuantumCircuit(qr_a, qr_b, qr_out)

    adder = HalfAdderGate(num_state_qubits)
    controlled_adder = adder.control()

    # build multiplication circuit
    for i in range(num_state_qubits):
        excess_qubits = max(0, num_state_qubits + i + 1 - num_result_qubits)
        if excess_qubits == 0:
            num_adder_qubits = num_state_qubits
            this_controlled = controlled_adder
        else:
            num_adder_qubits = num_state_qubits - excess_qubits + 1
            modular = ModularAdderGate(num_adder_qubits)
            this_controlled = modular.control()

        qr_list = [qr_a[i], *qr_b[:num_adder_qubits], *qr_out[i : num_state_qubits + i + 1 - excess_qubits]]
        qc.append(this_controlled, qr_list)

    qc.measure_all()
    qc.name = "hrs_cumulative_multiplier"

    return qc
