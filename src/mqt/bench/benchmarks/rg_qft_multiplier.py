# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""RG QFT Multiplier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from qiskit.synthesis import multiplier_qft_r17

if TYPE_CHECKING:
    from qiskit.circuit import QuantumCircuit


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Create a rg qft multiplier circuit.

    Arguments:
            num_qubits: Number of qubits of the returned quantum circuit, must be divisible by 4.

    Returns:
           QuantumCircuit: The constructed rg qft multiplier circuit.
    """
    if num_qubits % 4 or num_qubits < 4:
        msg = "num_qubits must be ≥ 4 and divisible by 4."
        raise ValueError(msg)

    num_state_qubits = num_qubits // 4

    qc = multiplier_qft_r17(num_state_qubits)
    qc.measure_all()
    qc.name = "rg_qft_multiplier"

    return qc
