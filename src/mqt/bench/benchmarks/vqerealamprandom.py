# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""VQE realamp ansatz benchmark definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from packaging.version import Version
from qiskit import version

if Version(version.get_version_info()) >= Version("1.3.2"):
    from qiskit.circuit.library import real_amplitudes
else:
    from qiskit.circuit.library import RealAmplitudes

    def real_amplitudes(num_qubits: int, entanglement: str = "full", reps: int = 3) -> RealAmplitudes:
        """RealAmplitudes (Qiskit < 1.3.2)."""
        return RealAmplitudes(num_qubits, entanglement=entanglement, reps=reps)


if TYPE_CHECKING:  # pragma: no cover
    from qiskit.circuit import QuantumCircuit


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing the RealAmplitudes ansatz with random parameter values.

    Arguments:
        num_qubits: number of qubits of the returned quantum circuit

    Returns:
        QuantumCircuit: a quantum circuit implementing the RealAmplitudes ansatz with random parameter values
    """
    rng = np.random.default_rng(10)
    qc = real_amplitudes(num_qubits, entanglement="full", reps=3)
    num_params = qc.num_parameters
    qc = qc.assign_parameters(2 * np.pi * rng.random(num_params))
    qc.measure_all()
    qc.name = "vqerealamprandom"

    return qc
