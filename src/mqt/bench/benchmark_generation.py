# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Module for the benchmark generation and benchmark retrieval."""

from __future__ import annotations

from enum import Enum, auto
from importlib import import_module
from typing import TYPE_CHECKING, cast

from qiskit import generate_preset_pass_manager
from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import Target
from typing_extensions import assert_never

from .targets.gatesets import get_target_for_gateset

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType

    from qiskit.transpiler import Target

from qiskit.circuit import SessionEquivalenceLibrary

from .targets.gatesets import ionq, rigetti


class BenchmarkLevel(Enum):
    """Enum representing different levels."""

    ALG = auto()
    INDEP = auto()
    NATIVEGATES = auto()
    MAPPED = auto()


def get_supported_benchmarks() -> list[str]:
    """Returns a list of all supported benchmarks."""
    return [
        "ae",
        "bv",
        "dj",
        "ghz",
        "graphstate",
        "grover",
        "qaoa",
        "qft",
        "qftentangled",
        "qnn",
        "qpeexact",
        "qpeinexact",
        "quarkcardinality",
        "quarkcopula",
        "qwalk",
        "randomcircuit",
        "shor",
        "vqerealamprandom",
        "vqesu2random",
        "vqetwolocalrandom",
        "wstate",
    ]


def get_module_for_benchmark(benchmark_name: str) -> ModuleType:
    """Returns the module for a specific benchmark."""
    return import_module("mqt.bench.benchmarks." + benchmark_name)


def _create_raw_circuit(
    benchmark: str | QuantumCircuit,
    circuit_size: int | None,
    benchmark_instance_name: str | None,
) -> QuantumCircuit:
    """Creates a raw quantum circuit based on the specified benchmark.

    This function generates a quantum circuit according to the specifications of the
    desired benchmark. It validates the provided benchmark name, and depending on the
    benchmark, it may require additional parameters such as a specific benchmark instance
    name or the circuit size.

    Arguments:
        benchmark: QuantumCircuit or name of the benchmark for which the circuit is to be created.
        circuit_size: Size of the circuit to be created, required for benchmarks other than "shor".
        benchmark_instance_name: Instance specification needed for the "shor" benchmark.

    Returns:
        QuantumCircuit: Constructed quantum circuit based on the given parameters.
    """
    if isinstance(benchmark, QuantumCircuit):
        return benchmark

    if benchmark not in get_supported_benchmarks():
        msg = f"'{benchmark}' is not a supported benchmark. Valid names: {get_supported_benchmarks()}"
        raise ValueError(msg)

    if benchmark == "shor":
        if not isinstance(benchmark_instance_name, str):
            msg = "`benchmark_instance_name` must be given for Shor benchmarks."
            raise ValueError(msg)
        lib = get_module_for_benchmark("shor")
        to_be_factored_number, a_value = lib.get_instance(benchmark_instance_name)
        return lib.create_circuit(to_be_factored_number, a_value)

    if not (isinstance(circuit_size, int) and circuit_size > 0):
        msg = "`circuit_size` must be a positive integer for this benchmark."
        raise ValueError(msg)
    lib = get_module_for_benchmark(benchmark)
    return lib.create_circuit(circuit_size)


def _validate_opt_level(opt_level: int) -> None:
    """Validate optimization level.

    Arguments:
        opt_level: User-defined optimization level.
    """
    if not 0 <= opt_level <= 3:
        msg = f"Invalid `opt_level` '{opt_level}'. Must be in the range [0, 3]."
        raise ValueError(msg)


def get_alg_benchmark(
    benchmark: str | QuantumCircuit,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
) -> QuantumCircuit:
    """Return an algorithm-level benchmark circuit.

    Arguments:
            benchmark: QuantumCircuit or name of the benchmark to be generated
            circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
            benchmark_instance_name: Input selection for some benchmarks, namely "shor"

    Returns:
            Qiskit::QuantumCircuit representing the raw benchmark circuit without any hardware-specific compilation or mapping.
    """
    return _create_raw_circuit(benchmark, circuit_size, benchmark_instance_name)


def get_indep_benchmark(
    benchmark: str | QuantumCircuit,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    opt_level: int = 2,
) -> QuantumCircuit:
    """Return a target-independent benchmark circuit.

    Arguments:
            benchmark: QuantumCircuit or name of the benchmark to be generated
            circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
            benchmark_instance_name: Input selection for some benchmarks, namely "shor"
            opt_level: Optimization level to be used by the transpiler.

    Returns:
            Qiskit::QuantumCircuit expressed in a generic basis gate set, still unmapped to any physical device.
    """
    _validate_opt_level(opt_level)

    qc = _create_raw_circuit(benchmark, circuit_size, benchmark_instance_name)
    return transpile(qc, optimization_level=opt_level, seed_transpiler=10)


def get_native_gates_benchmark(
    benchmark: str | QuantumCircuit,
    target: Target,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    opt_level: int = 2,
) -> QuantumCircuit:
    """Return a benchmark compiled to the target's native gate set.

    Arguments:
            benchmark: QuantumCircuit or name of the benchmark to be generated
            target: `~qiskit.transpiler.target.Target` for the benchmark generation
            circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
            benchmark_instance_name: Input selection for some benchmarks, namely "shor"
            opt_level: Optimization level to be used by the transpiler.

    Returns:
            Qiskit::QuantumCircuit whose operations are restricted to ``target``'s native gate set but are **not** yet qubit-mapped to a concrete device connectivity.
    """
    if target is None:
        msg = "`target` must be supplied for the native-gates level."
        raise ValueError(msg)

    _validate_opt_level(opt_level)

    qc = _create_raw_circuit(benchmark, circuit_size, benchmark_instance_name)

    if target.description == "clifford+t":
        from qiskit.transpiler import PassManager  # noqa: PLC0415
        from qiskit.transpiler.passes.synthesis import SolovayKitaev  # noqa: PLC0415

        # Transpile the circuit to single- and two-qubit gates including rotations
        clifford_t_rotations = get_target_for_gateset("clifford+t+rotations", num_qubits=circuit_size)
        compiled_for_sk = transpile(
            qc,
            target=clifford_t_rotations,
            optimization_level=opt_level,
            seed_transpiler=10,
        )
        # Synthesize the rotations to Clifford+T gates
        # Measurements are removed and added back after the synthesis to avoid errors in the Solovay-Kitaev pass
        pm = PassManager(SolovayKitaev())
        qc = pm.run(compiled_for_sk.remove_final_measurements(inplace=False))
        qc.measure_all()

    if "rigetti" in target.description:
        rigetti.add_equivalences(SessionEquivalenceLibrary)
    elif "ionq" in target.description:
        ionq.add_equivalences(SessionEquivalenceLibrary)
    pm = generate_preset_pass_manager(optimization_level=opt_level, target=target, seed_transpiler=10)
    pm.layout = None
    pm.routing = None
    pm.scheduling = None

    return pm.run(qc)


def get_mapped_benchmark(
    benchmark: str | QuantumCircuit,
    target: Target,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    opt_level: int = 2,
) -> QuantumCircuit:
    """Return a benchmark fully compiled and qubit-mapped to a device.

    Arguments:
            benchmark: QuantumCircuit or name of the benchmark to be generated
            target: `~qiskit.transpiler.target.Target` for the benchmark generation
            circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
            benchmark_instance_name: Input selection for some benchmarks, namely "shor"
            opt_level: Optimization level to be used by the transpiler.

    Returns:
            Qiskit::QuantumCircuit that has been decomposed and routed onto the connectivity described by ``target``.
    """
    if target is None:
        msg = "`target` must be supplied for the mapped level."
        raise ValueError(msg)

    _validate_opt_level(opt_level)

    qc = _create_raw_circuit(benchmark, circuit_size, benchmark_instance_name)

    if "rigetti" in target.description:
        rigetti.add_equivalences(SessionEquivalenceLibrary)
    elif "ionq" in target.description:
        ionq.add_equivalences(SessionEquivalenceLibrary)

    return transpile(
        qc,
        target=target,
        optimization_level=opt_level,
        seed_transpiler=10,
    )


def get_benchmark(
    benchmark: str | QuantumCircuit,
    level: BenchmarkLevel,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    opt_level: int | None = 2,
    target: Target | None = None,
) -> QuantumCircuit:
    """Returns one benchmark as a qiskit.QuantumCircuit object.

    Arguments:
        benchmark: QuantumCircuit or name of the benchmark to be generated
        level: Choice of level, either as a string ("alg", "indep", "nativegates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
        circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
        benchmark_instance_name: Input selection for some benchmarks, namely "shor"
        opt_level: Optimization level to be used by the transpiler.
        target: `~qiskit.transpiler.target.Target` for the benchmark generation (only used for "nativegates" and "mapped" level)

    Returns:
        Qiskit::QuantumCircuit object representing the benchmark with the selected options
    """
    if not isinstance(cast("object", level), BenchmarkLevel):
        allowed = ", ".join(f"BenchmarkLevel.{m.name}" for m in BenchmarkLevel)
        msg = f"Invalid benchmark level '{level}'. Must be one of: {allowed}."
        raise TypeError(msg)

    if level is BenchmarkLevel.ALG:
        return get_alg_benchmark(
            benchmark,
            circuit_size=circuit_size,
            benchmark_instance_name=benchmark_instance_name,
        )

    if opt_level is None:
        msg = "`opt_level` must be specified for indep, nativegates, or mapped level."
        raise ValueError(msg)
    _validate_opt_level(opt_level)
    opt_kw = {"opt_level": opt_level}

    if level is BenchmarkLevel.INDEP:
        return get_indep_benchmark(
            benchmark,
            circuit_size=circuit_size,
            benchmark_instance_name=benchmark_instance_name,
            **opt_kw,
        )
    if level is BenchmarkLevel.NATIVEGATES:
        return get_native_gates_benchmark(
            benchmark,
            target,
            circuit_size=circuit_size,
            benchmark_instance_name=benchmark_instance_name,
            **opt_kw,
        )
    if level is BenchmarkLevel.MAPPED:
        return get_mapped_benchmark(
            benchmark,
            target,
            circuit_size=circuit_size,
            benchmark_instance_name=benchmark_instance_name,
            **opt_kw,
        )

    assert_never(level)
