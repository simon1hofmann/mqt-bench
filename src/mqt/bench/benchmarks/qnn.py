# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Quantum Neural Network benchmark definition. Code is inspired by https://qiskit.org/ecosystem/machine-learning/stubs/qiskit_machine_learning.neural_networks.EstimatorQNN.html."""

from __future__ import annotations

import numpy as np
from packaging.version import Version
from qiskit import version
from qiskit.circuit import QuantumCircuit

if Version(version.get_version_info()) >= Version("1.3.2"):
    from qiskit.circuit.library import real_amplitudes, z_feature_map
else:
    from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap

    def real_amplitudes(num_qubits: int, reps: int = 1) -> RealAmplitudes:
        """RealAmplitudes (Qiskit < 1.3.2)."""
        return RealAmplitudes(num_qubits, reps=reps)

    def z_feature_map(feature_dimension: int) -> ZZFeatureMap:
        """ZZFeatureMap (Qiskit < 1.3.2)."""
        return ZZFeatureMap(feature_dimension=feature_dimension)


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing a Quantum Neural Network (QNN) with a ZZ FeatureMap and a RealAmplitudes ansatz.

    Arguments:
        num_qubits: number of qubits of the returned quantum circuit
    """
    feature_map = z_feature_map(feature_dimension=num_qubits)
    ansatz = real_amplitudes(num_qubits=num_qubits, reps=1)

    qc = QuantumCircuit(num_qubits)
    feature_map = feature_map.assign_parameters([1 for _ in range(feature_map.num_parameters)])

    rng = np.random.default_rng(10)
    ansatz = ansatz.assign_parameters(rng.random(ansatz.num_parameters) * 2 * np.pi)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)

    qc.name = "qnn"
    qc.measure_all()
    return qc
