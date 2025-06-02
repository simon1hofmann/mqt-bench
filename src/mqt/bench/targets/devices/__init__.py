# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Initialization of the devices module."""

from __future__ import annotations

import copy
import importlib
import importlib.resources as ir
from functools import cache
from typing import TYPE_CHECKING, cast

from . import _registry as device_registry
from ._registry import register_device

if TYPE_CHECKING:
    from pathlib import Path

    from qiskit.transpiler import Target

__all__ = [
    "get_available_device_names",
    "get_device",
    "register_device",
]

for entry in ir.files(__package__).iterdir():
    if (path := cast("Path", entry)).is_file() and path.suffix == ".py" and not path.stem.startswith("_"):
        importlib.import_module(f"{__package__}.{path.stem}")
        __all__ += [f"{path.stem}"]  # noqa: PLE0604


def get_available_device_names() -> list[str]:
    """Return a list of available device names."""
    return device_registry.device_names().copy()


@cache
def _get_device(device_name: str) -> Target:
    """Internal cacheable function to get a device by name.

    Arguments:
        device_name: Name of the device.
    """
    try:
        return device_registry.get_device_by_name(device_name)
    except KeyError:
        msg = f"Unknown device '{device_name}'. Available devices: {get_available_device_names()}"
        raise ValueError(msg) from None


def get_device(device_name: str) -> Target:
    """Get a deepcopy of a device by name.

    Arguments:
        device_name: Name of the device.
    """
    return copy.deepcopy(_get_device(device_name))
