"""Compilation functions to create benchmarks on different levels of abstraction using Qiskit."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit

    from .devices import Device, Provider

from qiskit import transpile

from .utils import get_openqasm_gates, save_as_qasm


def get_alg_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the algorithm level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)


    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if return_qc:
        return qc

    if qasm_format == "qasm2":
        msg = "'qasm2' is not supported for the algorithm level, please use 'qasm3' instead."
        raise ValueError(msg)
    filename_alg = target_filename or qc.name + "_alg_qiskit_" + str(num_qubits) + "_" + qasm_format

    path = Path(target_directory, filename_alg + ".qasm")

    if file_precheck and path.is_file():
        return True

    return save_as_qasm(qc=qc, filename=filename_alg, qasm_format="qasm3", target_directory=target_directory)


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool: ...


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-independent level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)


    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    filename_indep = target_filename or qc.name + "_indep_qiskit_" + str(num_qubits) + "_" + qasm_format

    path = Path(target_directory, filename_indep + ".qasm")
    if file_precheck and path.is_file():
        return True
    openqasm_gates = get_openqasm_gates()
    target_independent = transpile(qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10)

    if return_qc:
        return target_independent

    return save_as_qasm(
        qc=target_independent, filename=filename_indep, qasm_format=qasm_format, target_directory=target_directory
    )


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool: ...


def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        provider: determines the native gate set
        num_qubits: number of qubits
        opt_level: optimization level
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_native = (
            qc.name + "_nativegates_" + provider.provider_name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
        )
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True

    gate_set = provider.get_native_gates()
    compiled_without_architecture = transpile(
        qc, basis_gates=gate_set, optimization_level=opt_level, seed_transpiler=10
    )
    if return_qc:
        return compiled_without_architecture

    return save_as_qasm(
        qc=compiled_without_architecture,
        filename=filename_native,
        qasm_format=qasm_format,
        gate_set=gate_set,
        target_directory=target_directory,
    )


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool: ...


def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        device: target device
        opt_level: optimization level
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device.name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True

    c_map = device.coupling_map
    compiled_with_architecture = transpile(
        qc,
        optimization_level=opt_level,
        basis_gates=device.basis_gates,
        coupling_map=c_map,
        seed_transpiler=10,
    )
    if return_qc:
        return compiled_with_architecture

    return save_as_qasm(
        qc=compiled_with_architecture,
        filename=filename_mapped,
        qasm_format=qasm_format,
        gate_set=device.basis_gates,
        mapped=True,
        c_map=c_map,
        target_directory=target_directory,
    )
