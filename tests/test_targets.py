# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Test targets."""

from __future__ import annotations

import re

import pytest
from qiskit.transpiler import Target

from mqt.bench.targets.devices import get_available_device_names, get_device


@pytest.mark.parametrize(
    ("device_name", "num_qubits", "expected_2q_gate"),
    [
        ("ibm_falcon_27", 27, "cx"),
        ("ibm_falcon_127", 127, "cx"),
        ("ibm_eagle_127", 127, "ecr"),
        ("ibm_heron_133", 133, "cz"),
        ("ibm_heron_156", 156, "cz"),
    ],
)
def test_ibm_targets(device_name: str, num_qubits: int, expected_2q_gate: str) -> None:
    """Test structure and basic gate support for IBM targets."""
    target = get_device(device_name)

    assert isinstance(target, Target)
    assert target.description == device_name
    assert target.num_qubits == num_qubits

    # === Gate presence check ===
    expected_1q_gates = {"sx", "rz", "x", "measure"}
    assert expected_1q_gates.issubset(set(target.operation_names))
    assert expected_2q_gate in target.operation_names

    # === Validate available qubits for single-qubit gates
    for gate in expected_1q_gates:
        for (q,) in target[gate]:
            assert isinstance(q, int)
            # Optional: check that props are present (but allow None)
            props = target[gate][q,]
            assert props is not None

    # === Validate two-qubit gate connections
    for (q0, q1), props in target[expected_2q_gate].items():
        assert isinstance(q0, int)
        assert isinstance(q1, int)
        assert q0 != q1
        assert props is not None

    # === Validate measure connections
    for (q,) in target["measure"]:
        assert isinstance(q, int)
        props = target["measure"][q,]
        assert props is not None


@pytest.mark.parametrize(
    ("device_name", "entangling_gate"),
    [
        ("ionq_aria_25", "ms"),
        ("ionq_forte_36", "zz"),
    ],
)
def test_ionq_targets(device_name: str, entangling_gate: str) -> None:
    """Test the structure of the IonQ targets."""
    target = get_device(device_name)

    assert isinstance(target, Target)
    assert target.description == device_name
    assert target.num_qubits > 0

    # Check gate support
    assert "gpi" in target.operation_names
    assert "gpi2" in target.operation_names
    assert entangling_gate in target.operation_names
    assert "measure" in target.operation_names

    # Single-qubit gates should have properties for all qubits
    for op_name in ["gpi", "gpi2", "measure"]:
        for (qubit,) in target[op_name]:
            props = target[op_name][qubit,]
            assert props.duration >= 0
            assert props.error >= 0

    # Two-qubit gates should have connectivity and properties
    for (q1, q2), props in target[entangling_gate].items():
        assert q1 != q2
        assert props.duration > 0
        assert props.error > 0


@pytest.mark.parametrize(
    ("device_name", "num_qubits"),
    [
        ("iqm_crystal_5", 5),
        ("iqm_crystal_20", 20),
        ("iqm_crystal_54", 54),
    ],
)
def test_iqm_targets(device_name: str, num_qubits: int) -> None:
    """Test the structure of the IQM targets."""
    target = get_device(device_name)

    assert isinstance(target, Target)
    assert target.description == device_name
    assert target.num_qubits == num_qubits

    # Expected gate types
    expected_ops = {"r", "cz", "measure"}
    assert expected_ops.issubset(set(target.operation_names))

    # Check single-qubit RGate properties
    for (qubit,) in target["r"]:
        props = target["r"][qubit,]
        assert props.duration > 0
        assert 0 <= props.error < 1

    # Check measurement properties
    for (qubit,) in target["measure"]:
        props = target["measure"][qubit,]
        assert props.duration > 0
        assert 0 <= props.error < 1

    # Check CZ gate symmetry and properties
    for (q1, q2), props in target["cz"].items():
        assert q1 != q2
        assert props.duration > 0
        assert 0 <= props.error < 1
        # Also ensure the reverse pair is present (symmetry) for iqm_crystal_5
        if device_name == "iqm_crystal_5":
            assert (q2, q1) in target["cz"]


def test_quantinuum_target() -> None:
    """Test the structure of the Quantinuum H2 target device."""
    target = get_device("quantinuum_h2_56")

    # Basic metadata
    assert isinstance(target, Target)
    assert target.description == "quantinuum_h2_56"
    assert target.num_qubits == 56  # adjust if your calibration changes

    # Ensure all expected gates are supported
    expected_gates = {"rx", "ry", "rz", "rzz", "measure"}
    assert expected_gates.issubset(set(target.operation_names))

    # === Single-qubit gates ===
    for op in ["rx", "ry", "rz"]:
        insts = target[op]
        assert all(len(qargs) == 1 for qargs in insts), f"{op} not single-qubit"
        for props in insts.values():
            assert 0 <= props.error < 1

    # === Measurement ===
    insts = target["measure"]
    assert all(len(qargs) == 1 for qargs in insts)
    for props in insts.values():
        assert 0 <= props.error < 1

    # === Two-qubit gates ===
    insts = target["rzz"]
    assert all(len(qargs) == 2 for qargs in insts)
    for (q0, q1), props in insts.items():
        assert q0 != q1
        assert 0 <= props.error < 1

    # Symmetry check (if assumed)
    # This is optional, depending on your calibration assumption
    for q0, q1 in insts:
        assert (q1, q0) in insts


def test_rigetti_target() -> None:
    """Test the structure of the Rigetti Ankaa 3 target device."""
    target = get_device("rigetti_ankaa_84")

    assert isinstance(target, Target)
    assert target.description == "rigetti_ankaa_84"
    assert target.num_qubits == 84

    expected_single_qubit_gates = {
        "rxpi",
        "rxpi2",
        "rxpi2dg",
        "rz",
        "measure",
    }
    expected_two_qubit_gates = {"iswap"}

    assert expected_single_qubit_gates.issubset(set(target.operation_names))
    assert any(g in target.operation_names for g in expected_two_qubit_gates)

    # === Single-qubit gate properties ===
    for gate in expected_single_qubit_gates:
        if gate not in target.operation_names:
            continue
        for props in target[gate].values():
            assert 0 <= props.error < 1

    # === Two-qubit gate properties ===
    for gate in expected_two_qubit_gates:
        if gate not in target.operation_names:
            continue
        for (q0, q1), props in target[gate].items():
            assert q0 != q1
            assert 0 <= props.error < 1

    # === Readout fidelity ===
    if "measure" in target.operation_names:
        for props in target["measure"].values():
            assert 0 <= props.error < 1


def test_get_unknown_device() -> None:
    """Test the get_device function with an unknown device name."""
    device = "unknown_device"
    match = re.escape(f"Unknown device '{device}'. Available devices: {get_available_device_names()}")

    with pytest.raises(ValueError, match=match):
        get_device(device)
