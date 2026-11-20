# ShipOps Phase 0 — Setup Report

## 1. Environment

- Host OS: Windows 11
- Linux environment: Ubuntu 26.04.1 LTS on WSL2
- Architecture: linux/amd64
- WSL version: 3.0.5.0
- Host RAM: 16 GB DDR5
- WSL reported memory: 7.6 GiB
- Host C: drive free space: 174 GB (reported)
- WSL filesystem reported available space: 955 GiB
- Workspace: ~/projects/shipops-challenge

Note: WSL virtual filesystem capacity is not the same
as available physical space on the Windows host.

## 2. Tool Versions

| Tool | Verified Version |
| --- | --- |
| Git | 2.53.0 |
| GitHub CLI | 2.46.0 |
| Python | 3.14.4 |
| curl | 8.18.0 |
| jq | 1.8.1 |
| Docker Client | 29.9.3 |
| Docker Engine | 29.9.3 |
| Docker Desktop | 4.99.0 |
| kubectl | v1.37.2 |
| kind | v0.33.0 |
| Helm | v4.3.2 |
| Kubernetes test cluster | v1.37.0 |

## 3. Preflight Results

| Test | Status | Actual Result |
| --- | --- | --- |
| git --version | PASS | Git 2.53.0 |
| python3 execution | PASS | Python OK |
| curl GitHub connectivity | PASS | HTTP/2 200 |
| jq JSON parsing | PASS | JSON parsed |
| docker version | PASS | Client and Server responded |
| docker run --rm hello-world | PASS | Hello from Docker! |
| kubectl version --client | PASS | v1.37.2 |
| kind version | PASS | v0.33.0 |
| helm version --short | PASS | v4.3.2 |
| kind cluster creation | PASS | prep-check created |
| kubectl get nodes | PASS | Node Ready |
| kind cluster deletion | PASS | No kind clusters found |
| GitHub authentication | PASS | GitHub CLI logged in |
| Public repository visibility | PASS | Public repository verified |
| First Git commit and push | PENDING | Not completed yet |
| Second Git commit and push | PENDING | Not completed yet |
| GitHub Actions availability | NOT CHECKED | Pending |
| AI coding agent execution | BLOCKER | See section 4 |

## 4. AI Coding Agent

Attempted agent: GitHub Copilot CLI

Authentication status: Not fully verified
File editing test: NOT RUN
File reading test: NOT RUN
Terminal execution test: NOT RUN

Observed error:

Failed to load models:
HTTP 403 unauthorized:
not authorized to use this Copilot feature

Reproduction:
1. Open Ubuntu terminal.
2. Navigate to ~/projects/shipops-agent-test.
3. Start the Copilot CLI.
4. Attempt to use its coding-agent features.
5. Model loading returned HTTP 403.

Workaround considered:
OpenAI Codex CLI as an alternative coding agent.

Remaining impact:
The mandatory AI agent verification has not passed.

## 5. Temporary Kubernetes Cluster Evidence

Command:
kind create cluster --name prep-check --wait 180s

Result:
Cluster created.
Control plane Ready after 16 seconds.

Command:
kubectl --context kind-prep-check get nodes

Result:
prep-check-control-plane Ready control-plane v1.37.0

Command:
kind delete cluster --name prep-check

Result:
Deleted nodes: ["prep-check-control-plane"]

Final check:
kind get clusters

Result:
No kind clusters found.

## 6. GitHub Repository

Public URL:
https://github.com/Badraghi/shipops-challenge

Default branch: main
Git transport: HTTPS
GitHub CLI authentication: PASS

First commit/push: PENDING
Second commit/push: PENDING
GitHub Actions: NOT CHECKED

## 7. Issues and Security

Previously observed Docker issues:
- Docker socket permission denied.
- Docker Hub image pull returned RBAC access denied.

Current impact:
Both issues were resolved before the final Docker test.
The exact remediation steps were not recorded.

Unresolved issue:
AI coding agent authorization and execution testing.

Security:
- No API tokens or credentials intentionally included.
- No private SSH keys included.
- No .env files intentionally included.
- Agent testing remains incomplete.

## 8. Final Status

Environment and Kubernetes readiness: PASS
GitHub submission: IN PROGRESS
AI coding agent: BLOCKER

Overall Phase 0 completion: INCOMPLETE
