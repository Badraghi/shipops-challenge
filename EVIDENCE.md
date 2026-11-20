# ShipOps Phase 1 - Evidence

Record actual commands and outputs **only after executing them**. Do not mark proposed tests as PASS.

## Milestone 1: API, automated tests and Docker

GET /healthz
Status: PASS
HTTP Status: 200
Response: {"status":"alive"}

GET /version
Status: PASS
HTTP Status: 200
Response: {"version":"step1"}

GET /readyz
Status: PASS (expected behavior before PostgreSQL deployment)
HTTP Status: 503
Response: {"detail":"database unavailable"}

Explanation:
PostgreSQL has not been deployed yet.
The readiness endpoint correctly reports that the
application is not ready to serve database requests.
Status: PASS (local API and Docker checks only)

- Git source commit: PENDING
- `python -m pytest -q`: PASS - 7 passed, 1 warning in 0.21s
- Docker image: PASS - shipops-api:step1 exists (SHA256 f3a72c195fb5...)
- Docker container: PASS - shipops-api-step1 Up (healthy), port 8000
- `GET /healthz`: HTTP 200 - {"status":"alive"}
- `GET /version`: HTTP 200 - {"version":"step1"}
- `GET /readyz`: HTTP 503 - {"detail":"database unavailable"} (expected before PostgreSQL)

Automated tests:
Command: python -m pytest -q
Result: PASS
Output: 7 passed

Docker image build:
Status: PASS
Image: shipops-api:step1
Result: Build completed successfully.

## Milestone 2: kind, Helm, PostgreSQL and PVC

Status: NOT STARTED

- Two API Pods Ready: NOT TESTED
- PostgreSQL item ID before restart: NOT TESTED
- PostgreSQL item ID after restart: NOT TESTED
- `kubectl port-forward` access: NOT TESTED

## Milestone 3: GitHub Actions, GHCR and Argo CD

Status: NOT STARTED

- Successful GitHub Actions run URL: PENDING
- Published GHCR image (unique SHA tag): PENDING
- Git-managed image update commit: PENDING
- Argo CD Sync: NOT TESTED
- `GET /version` after delivery: NOT TESTED

## Milestone 4: Reliability, rollback and metrics

Status: NOT STARTED

- Rolling update evidence: PENDING
- Pod termination under traffic: NOT TESTED
- Previous release ID: PENDING
- New release ID: PENDING
- Rollback using Git: NOT TESTED
- Item readable after rollback: NOT TESTED
- Metrics scraper and query output: NOT TESTED

## Chronological working commits

1. PENDING: API and local tests
2. PENDING: Kubernetes + PostgreSQL
3. PENDING: delivery pipeline + Argo CD
4. PENDING: reliability and metrics
5. PENDING: final acceptance evidence

## Known blockers / incomplete checks

- Real database is not deployed at Milestone 1; item persistence cannot yet be claimed.

## Milestone 1 — Actual HTTP Smoke Test Results

Environment:
- Ubuntu 26.04.1 LTS on WSL2
- API address: http://127.0.0.1:8000
- Release identifier: step1

### Test 1: Application Health

Command:
curl -sS -w '\nHTTP_STATUS: %{http_code}\n' http://127.0.0.1:8000/healthz

Actual output:
{"status":"alive"}
HTTP_STATUS: 200

Result: PASS

### Test 2: Application Version

Command:
curl -sS -w '\nHTTP_STATUS: %{http_code}\n' http://127.0.0.1:8000/version

Actual output:
{"version":"step1"}
HTTP_STATUS: 200

Result: PASS

### Test 3: Application Readiness

Command:
curl -sS -w '\nHTTP_STATUS: %{http_code}\n' http://127.0.0.1:8000/readyz

Actual output:
{"detail":"database unavailable"}
HTTP_STATUS: 503

Result: EXPECTED BEFORE DATABASE DEPLOYMENT

Explanation:
PostgreSQL has not been deployed in this milestone.
The readiness endpoint correctly reports that the
application is not ready for database-dependent requests.

Full database readiness verification: PENDING

