# ShipOps — Phase 0 Environment Readiness

This public repository contains the environment preparation
evidence for ShipOps Phase 0.

## Workstation

- Host operating system: Windows 11
- Development environment: Ubuntu 26.04.1 LTS on WSL2
- Architecture: x86_64
- Host RAM: 16 GB DDR5
- Docker: Docker Desktop with WSL2 integration

## Installed Toolchain

- Git and GitHub CLI
- Docker
- kubectl
- kind
- Helm
- Python 3
- curl and jq

## Verification

Docker hello-world completed successfully.

A temporary Kubernetes cluster named `prep-check`
was created, its node reached Ready, and the cluster
was successfully deleted.

See [SETUP_REPORT.md](SETUP_REPORT.md) for detailed
versions, checks, results and unresolved issues.

## Project Scope

This repository is reserved for the upcoming
four-hour ShipOps engineering task.

Phase 0 is environment preparation only.
No production application, Kubernetes deployment,
CI/CD pipeline or GitOps implementation is included.
