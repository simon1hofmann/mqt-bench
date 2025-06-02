# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Handles the available native gatesets."""

from __future__ import annotations

import copy
import importlib
import importlib.resources as ir
from functools import cache
from typing import TYPE_CHECKING, cast

from qiskit.circuit import Parameter
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.providers.fake_provider import GenericBackendV2

from . import _registry as gateset_registry
from ._registry import register_gateset
from .ionq import GPI2Gate, GPIGate, MSGate, ZZGate
from .rigetti import RXPI2DgGate, RXPI2Gate, RXPIGate

if TYPE_CHECKING:
    from pathlib import Path

    from qiskit.transpiler import Target

__all__ = [
    "get_available_gateset_names",
    "get_gateset",
    "get_target_for_gateset",
    "register_gateset",
]

for entry in ir.files(__package__).iterdir():
    if (path := cast("Path", entry)).is_file() and path.suffix == ".py" and not path.stem.startswith("_"):
        importlib.import_module(f"{__package__}.{path.stem}")
        __all__ += [f"{path.stem}"]  # noqa: PLE0604


def get_available_gateset_names() -> list[str]:
    """Return a list of available gateset names."""
    return gateset_registry.gateset_names().copy()


@cache
def _get_gateset(gateset_name: str) -> list[str]:
    """Internal cacheable function to return the gateset for a given gateset name.

    Arguments:
        gateset_name: Name of the gateset.
    """
    try:
        return gateset_registry.get_gateset_by_name(gateset_name)
    except KeyError:
        msg = f"Unknown gateset '{gateset_name}'. Available gatesets: {get_available_gateset_names()}"
        raise ValueError(msg) from None


def get_gateset(gateset_name: str) -> list[str]:
    """Return the gateset for a given gateset name.

    Arguments:
        gateset_name: Name of the gateset.
    """
    return _get_gateset(gateset_name).copy()


@cache
def _get_target_for_gateset(name: str, num_qubits: int) -> Target:
    """Return the Target object for a given native gateset name."""
    gates = get_gateset(name)

    standard_gates = []
    other_gates = []
    for gate in gates:
        if gate in get_standard_gate_name_mapping():
            standard_gates.append(gate)
        else:
            other_gates.append(gate)
    backend = GenericBackendV2(num_qubits=num_qubits, basis_gates=standard_gates)
    target = backend.target
    target.description = name

    for gate in other_gates:
        alpha = Parameter("alpha")
        beta = Parameter("beta")
        gamma = Parameter("gamma")
        if gate == "gpi":
            target.add_instruction(GPIGate(alpha))
        elif gate == "gpi2":
            target.add_instruction(GPI2Gate(alpha))
        elif gate == "ms":
            target.add_instruction(MSGate(alpha, beta, gamma))
        elif gate == "zz":
            target.add_instruction(ZZGate(alpha))
        elif gate == "rxpi":
            target.add_instruction(RXPIGate())
        elif gate == "rxpi2":
            target.add_instruction(RXPI2Gate())
        elif gate == "rxpi2dg":
            target.add_instruction(RXPI2DgGate())
        else:
            msg = f"Gate '{gate}' not found in available gatesets."
            raise ValueError(msg) from None

    return target


def get_target_for_gateset(name: str, num_qubits: int) -> Target:
    """Return a deepcopy of a Target object for a given native gateset name."""
    return copy.deepcopy(_get_target_for_gateset(name, num_qubits))
