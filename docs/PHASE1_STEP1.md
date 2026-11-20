# Phase 1 / Milestone 1 - API, tests, Docker

This is an instruction sheet for the first working increment, not acceptance evidence.

## 1. From Ubuntu (WSL2), in your existing cloned repository

```bash
cd ~/projects/shipops-challenge
pwd
ls -la app requirements.txt Dockerfile
```

The files from this archive should be directly inside this repository, alongside the existing Phase 0 files. Keep `.git/`, `.gitignore`, and `SETUP_REPORT.md`.

## 2. Create a venv and install development dependencies

```bash
sudo apt update
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Do not commit `.venv/`. It is ignored by your existing `.gitignore`.

## 3. Build and run Docker image

```bash
docker build --build-arg RELEASE_VERSION=step1 -t shipops-api:step1 .
docker run -d --rm --name shipops-api-step1 -p 127.0.0.1:8000:8000 shipops-api:step1
curl -i http://127.0.0.1:8000/healthz
curl -i http://127.0.0.1:8000/version
curl -i http://127.0.0.1:8000/readyz
curl -s http://127.0.0.1:8000/metrics | grep 'shipops_http_requests_total' | head
```

At Milestone 1, 503 from `/readyz` is expected because PostgreSQL is not yet deployed. Do NOT claim complete database API readiness yet.

Stop the test container:

```bash
docker stop shipops-api-step1
```

## 4. Record observed outputs in EVIDENCE.md, then commit and push

```bash
git status --short
git add app tests requirements.txt requirements-dev.txt Dockerfile .dockerignore EVIDENCE.md DECISIONS.md docs/PHASE1_STEP1.md
git diff --cached --stat
git diff --cached --check
git commit -m "feat: implement tested ShipOps API and Docker image"
git push origin main
```

If commands fail, STOP, preserve the error text and report it before pushing a claimed success.
