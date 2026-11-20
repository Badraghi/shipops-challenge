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
