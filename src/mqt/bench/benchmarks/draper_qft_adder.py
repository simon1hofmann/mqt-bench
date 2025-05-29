# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Draper QFT Adder."""

from __future__ import annotations

from qiskit.circuit import QuantumCircuit
from qiskit.synthesis import adder_qft_d00


def create_circuit(num_qubits: int, kind: str | None = "half") -> QuantumCircuit:
    """Create a draper qft adder circuit.

    Arguments:
            num_qubits: Number of qubits of the returned quantum circuit
            kind: The kind of adder, can be ``"half"`` for a half adder or
               ``"fixed"`` for a fixed-sized adder. A half adder contains a carry-out to represent
               the most-significant bit, but the fixed-sized adder doesn't and hence performs
               addition modulo ``2 ** num_state_qubits``.

    Returns:
           QuantumCircuit: The constructed draper qft adder circuit.
    """
    if kind == "half":
        if num_qubits % 2 == 0 or num_qubits < 3:
            msg = "num_qubits must be an odd integer ≥ 3."
            raise ValueError(msg)
        num_state_qubits = (num_qubits - 1) // 2
    elif kind == "fixed":
        if num_qubits % 2 or num_qubits < 2:
            msg = "num_qubits must be an even integer ≥ 2."
            raise ValueError(msg)
        num_state_qubits = num_qubits // 2
    else:
        msg = "kind must be 'half' or 'fixed'."
        raise ValueError(msg)

    gate = adder_qft_d00(num_state_qubits, kind)

    qc = QuantumCircuit(gate.num_qubits)
    qc.append(gate, qc.qubits)
    qc.measure_all()
    qc.name = "draper_qft_adder"

    return qc
