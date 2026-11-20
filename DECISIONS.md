# ShipOps Phase 1 - Engineering Decisions

These are planned design choices, not proof that deployment has succeeded.

## Architecture

- Python and FastAPI for a small documented REST API and straightforward automated testing.
- PostgreSQL as the only persistent data store, matching the challenge requirement.
- `DATABASE_URL` is injected via the environment; never commit real database credentials.
- A shared PostgreSQL database allows multiple stateless API replicas.
- `/healthz` is independent of the database; `/readyz` queries PostgreSQL.
- `/version` is based on the `RELEASE_VERSION` environment variable so deployment can bind it to a Git revision.
- `prometheus_client` exports request, error and duration metrics under `/metrics`.
- Docker image uses a non-root Unix user.

## Scope and limitations

- Phase 1's first increment runs isolated HTTP tests with a fake store. This is NOT proof of persistence.
- The database table `items` will be provisioned by the PostgreSQL installation in Milestone 2.
- The Docker base image and Python dependency ranges are not yet pinned by content digest or lockfile.
- Do not use a mutable `latest` tag for CI-delivered images; use a commit SHA.
- AI assistance: ChatGPT helped draft the initial implementation. The user elected not to install a separate AI coding agent.

## Failures and accepted/rejected suggestions

- Record observed failures, tried corrections, and the actual effect here during the live work.
- Never claim a suggested fix was executed unless it was actually executed.


## Milestone 2 - Problems and Fixes

### Problem 1: Invalid Helm YAML

Observed problem:
PostgreSQL Deployment YAML contained invalid quotes
in the readiness probe command.

Result:
helm lint and helm template failed.

Fix:
Corrected the YAML quoting.

Verification:
Helm release later reached deployed status,
revision 2.

### Problem 2: PostgreSQL ImagePullBackOff

Observed problem:
The kind node received HTTP 403 Forbidden while
pulling postgres:17-alpine from Docker Hub.

Fix:
Pulled the image through Docker Desktop and loaded
it into kind:

docker pull postgres:17-alpine
kind load docker-image postgres:17-alpine --name shipops

Verification:
PostgreSQL reached 1/1 Ready.
Both API replicas reached Ready.

### Database Persistence

An item with ID 1 was created and retrieved.

The PostgreSQL Pod was deleted and replaced.

The same item remained readable afterward.

Limitation:
Data survival after deleting the entire kind
cluster was not verified.
