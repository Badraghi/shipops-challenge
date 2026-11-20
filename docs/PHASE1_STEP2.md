# Phase 1 / Milestone 2: kind + Helm + PostgreSQL (local)

This is a procedure, not proof of success. Fill EVIDENCE.md with actual outputs.

## Initial requirements
Docker Desktop with Ubuntu WSL Integration, kind, kubectl, Helm 4; local image `shipops-api:step1` already built.

## Bootstrap (WSL Ubuntu terminal)

```bash
cd ~/projects/shipops-challenge
bash scripts/bootstrap-kind.sh
```

The cluster is called `shipops`. Do not delete it after the test: it will be used for Argo CD in the following milestone.

## Create namespace and database secret

```bash
bash scripts/create-db-secret.sh
kubectl --context kind-shipops -n shipops get secret shipops-db-auth -o name
```

Never print or commit the secret values. This is a demo secret stored in the cluster, not in Git.

## Load local Docker image into kind

```bash
kind load docker-image shipops-api:step1 --name shipops
```

## Check Helm templates and install

```bash
helm lint helm/shipops
helm template shipops helm/shipops --namespace shipops > /tmp/shipops-rendered.yaml
helm upgrade --install shipops helm/shipops --namespace shipops --kube-context kind-shipops --wait --timeout 6m
kubectl --context kind-shipops -n shipops get pods -o wide
kubectl --context kind-shipops -n shipops get pvc
kubectl --context kind-shipops -n shipops get svc
```

Expect two API Pods Ready, one PostgreSQL Pod Ready, PVC Bound. PostgreSQL schema is installed only on FIRST initialization of an empty data directory; existing PVCs will not re-run init SQL.

## Access service from local laptop

First stop the standalone Docker test container if using TCP 8000:

```bash
docker stop shipops-api-step1
```

In separate Terminal A:

```bash
kubectl --context kind-shipops -n shipops port-forward svc/shipops-api 8000:8000
```

In Terminal B:

```bash
curl -sS -w '\nHTTP_STATUS: %{http_code}\n' http://127.0.0.1:8000/readyz
curl -sS -w '\nHTTP_STATUS: %{http_code}\n' -H 'Content-Type: application/json' -d '{"name":"persistent-notebook"}' http://127.0.0.1:8000/items
```

Record created ID (do not assume ID=1). Verify retrieval with `/items/<actual-id>`.

## Restart PostgreSQL Pod; verify PVC persistence

```bash
kubectl --context kind-shipops -n shipops delete pod -l app.kubernetes.io/name=shipops-postgres
kubectl --context kind-shipops -n shipops rollout status deployment/shipops-postgres --timeout=180s
kubectl --context kind-shipops -n shipops get pvc
```

After the pod is Ready, fetch `/items/<actual-id>` again and verify the same stored name. If service request is temporarily unavailable during the restart, repeat after readiness returns 200.

## Evidence and commit/push

Record actual outputs under Milestone 2 in `EVIDENCE.md`. Never invent success or include secret values.

```bash
git add helm/shipops scripts/bootstrap-kind.sh scripts/create-db-secret.sh docs/PHASE1_STEP2.md EVIDENCE.md DECISIONS.md
 git diff --cached --stat
 git diff --cached --check
 git commit -m "feat: deploy ShipOps with Helm PostgreSQL and persistent storage"
 git push origin main
```

**Do not delete the kind cluster.** Reuse it for Argo CD in Milestone 3.
