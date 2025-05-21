# Changelog

All notable changes to this project will be documented in this file.

The format is based on a mixture of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Common Changelog](https://common-changelog.org).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html), with the exception that minor releases may include breaking changes.

## [Unreleased]

### 🚀 Features and Enhancements

- ✨ Added `clifford+t` gateset @simon1hofmann (#555)
- 🎨 Removed `Provider` and improved `Device` Structure @simon1hofmann (#549)
- 🎨 Refactored Implementation of Shor's Benchmark @simon1hofmann (#548)
- ✨ Added two further benchmarks from BMW's QUARK @nquetschlich (#541)
- ♻️ Refactored output module @nquetschlich (#540)
- 🔥 Removed the generation logic @nquetschlich (#538)
- ✨ Introduce `Hatchling` and `dependency-groups` @nquetschlich (#530)
- ✨ Re-add support for Python 3.9 @simon1hofmann (#531)
- 🔥 Removed `TKET` dependency @simon1hofmann (#519)
- ✨ Added QASM3 support @simon1hofmann (#518)
- 🎨 Miscellaneous Fixes @simon1hofmann (#509)
- 🔥 Removed Placement Parameter for TKET Mapped Benchmarks @simon1hofmann (#510)
- 🚚 Renamed Random Circuit and VQE Ansatz Circuit Benchmarks @simon1hofmann (#508)
- 🔥 Removed all Benchmarks relying on `qiskit_optimization`, `qiskit_nature`, and `qiskit_algorithm` Dependencies @simon1hofmann (#507)
- 🎨 Re-implemented AE without Qiskit Application Modules @simon1hofmann (#506)
- ✨ Added Bernstein-Vazirani Algorithm @simon1hofmann (#505)
- 🔥 Removed the `benchviewer` and `evaluation` modules @burgholzer (#504)

### 📄 Documentation

- 📝 Switched from `.rst` to `.md` for documentation @simon1hofmann (#559)
- ✨ Move to MQT GitHub Orga and Re-Branding @simon1hofmann (#544)
- 📝 Update README and resource links due to repository migration @Drewniok (#543)

### 📦 Packaging

- ✨ Introduce `Hatchling` and `dependency-groups` @nquetschlich (#530)

### 🤖 CI

- 🔥 Server deployment for versions \<2 @nquetschlich (#556)
- ✅ Test up to Python 3.13 @simon1hofmann (#533)
- 👷Adjusted workflow urls @nquetschlich (#500)
- 🚨 Added another filter warning @nquetschlich (#489)
- 📌 Restricted qiskit-aer dependency @nquetschlich (#481)

### ⬆️ Dependencies

<details>
<summary>72 changes</summary>

- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#563)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.10 @[renovate[bot]](https://github.com/apps/renovate) (#561)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#558)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.9 @[renovate[bot]](https://github.com/apps/renovate) (#557)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#552)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.8 @[renovate[bot]](https://github.com/apps/renovate) (#550)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.32.0 @[renovate[bot]](https://github.com/apps/renovate) (#551)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#547)
- ⬆️👨‍💻 Update munich-quantum-toolkit/workflows action to v1.9 @[renovate[bot]](https://github.com/apps/renovate) (#546)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.7 @[renovate[bot]](https://github.com/apps/renovate) (#545)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#537)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.6 @[renovate[bot]](https://github.com/apps/renovate) (#535)
- ✨ Introduce `Hatchling` and `dependency-groups` @nquetschlich (#530)
- ✨ Re-add support for Python 3.9 @simon1hofmann (#531)
- 🔥 Removed `TKET` dependency @simon1hofmann (#519)
- 🎨 Miscellaneous Fixes @simon1hofmann (#509)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#517)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.33.0 @[renovate[bot]](https://github.com/apps/renovate) (#516)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.5 @[renovate[bot]](https://github.com/apps/renovate) (#514)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.31.1 @[renovate[bot]](https://github.com/apps/renovate) (#515)
- ⬆️🪝 update pre-commit hooks @[pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci) (#503)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#502)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.4 @[renovate[bot]](https://github.com/apps/renovate) (#501)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#499)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.32.1 @[renovate[bot]](https://github.com/apps/renovate) (#497)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.31.1 @[renovate[bot]](https://github.com/apps/renovate) (#496)
- ⬇️🐍 Added upper cap because of fake backends @nquetschlich (#493)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#492)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.2 @[renovate[bot]](https://github.com/apps/renovate) (#494)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.30.2 @[renovate[bot]](https://github.com/apps/renovate) (#490)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.0 @[renovate[bot]](https://github.com/apps/renovate) (#491)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#488)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.31.3 @[renovate[bot]](https://github.com/apps/renovate) (#486)
- ⬆️🪝 Update pre-commit hook rbubley/mirrors-prettier to v3.5.3 @[renovate[bot]](https://github.com/apps/renovate) (#487)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.30.1 @[renovate[bot]](https://github.com/apps/renovate) (#485)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.10 @[renovate[bot]](https://github.com/apps/renovate) (#484)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.6 @[renovate[bot]](https://github.com/apps/renovate) (#473)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#483)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.30.0 @[renovate[bot]](https://github.com/apps/renovate) (#482)
- ⬆️🪝 Update pre-commit hook pre-commit/mirrors-mypy to v1.15.0 @[renovate[bot]](https://github.com/apps/renovate) (#474)
- ⬆️🪝 Update pre-commit hook rbubley/mirrors-prettier to v3.5.2 @[renovate[bot]](https://github.com/apps/renovate) (#479)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.29.10 @[renovate[bot]](https://github.com/apps/renovate) (#478)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.31.2 @[renovate[bot]](https://github.com/apps/renovate) (#480)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#472)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.29.5 @[renovate[bot]](https://github.com/apps/renovate) (#470)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.4 @[renovate[bot]](https://github.com/apps/renovate) (#469)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.31.1 @[renovate[bot]](https://github.com/apps/renovate) (#471)
- ⬆️👨‍💻 Update cda-tum/mqt-workflows action to v1.7 @[renovate[bot]](https://github.com/apps/renovate) (#466)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#467)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#462)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.3 @[renovate[bot]](https://github.com/apps/renovate) (#465)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.2 @[renovate[bot]](https://github.com/apps/renovate) (#464)
- ⬆️🪝 Update pre-commit hook python-jsonschema/check-jsonschema to v0.31.0 @[renovate[bot]](https://github.com/apps/renovate) (#460)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.1 @[renovate[bot]](https://github.com/apps/renovate) (#458)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1 @[renovate[bot]](https://github.com/apps/renovate) (#461)
- ⬆️🪝 update pre-commit hooks @[pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci) (#457)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#456)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#455)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.4 @[renovate[bot]](https://github.com/apps/renovate) (#452)
- ⬆️🪝 Update pre-commit hook pre-commit/mirrors-mypy to v1.14.0 @[renovate[bot]](https://github.com/apps/renovate) (#454)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.28.4 @[renovate[bot]](https://github.com/apps/renovate) (#453)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#451)
- ⬆️👨‍💻 Update actions/attest-build-provenance action to v2.1.0 @[renovate[bot]](https://github.com/apps/renovate) (#450)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.28.3 @[renovate[bot]](https://github.com/apps/renovate) (#449)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.3 @[renovate[bot]](https://github.com/apps/renovate) (#448)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#447)
- ⬆️🪝 Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.2 @[renovate[bot]](https://github.com/apps/renovate) (#442)
- ⬆️🪝 Update pre-commit hook sirosen/texthooks to v0.6.8 @[renovate[bot]](https://github.com/apps/renovate) (#445)
- ⬆️🪝 Update pre-commit hook rbubley/mirrors-prettier to v3.4.2 @[renovate[bot]](https://github.com/apps/renovate) (#444)
- ⬆️👨‍💻 Update actions/attest-build-provenance action to v2 @[renovate[bot]](https://github.com/apps/renovate) (#446)
- ⬆️🪝 Update pre-commit hook crate-ci/typos to v1.28.2 @[renovate[bot]](https://github.com/apps/renovate) (#443)
- ⬆️🐍 Lock file maintenance @[renovate[bot]](https://github.com/apps/renovate) (#436)
</details>

_If you are upgrading: please see [`UPGRADING.md`](UPGRADING.md#unreleased)._

_📚 Refer to the [GitHub Release Notes](https://github.com/munich-quantum-toolkit/bench/releases) for previous changelogs._

[unreleased]: https://github.com/munich-quantum-toolkit/core/compare/v1.1.9...HEAD
