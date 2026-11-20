#!/usr/bin/env bash
set -euo pipefail
for bin in kind kubectl docker; do command -v "$bin" >/dev/null || { echo "Missing $bin" >&2; exit 1; }; done
docker info >/dev/null
if kind get clusters | grep -qx 'shipops'; then
  echo "Cluster shipops already exists; not recreating it."
else
  kind create cluster --name shipops --wait 180s
fi
kubectl --context kind-shipops create namespace shipops --dry-run=client -o yaml | kubectl --context kind-shipops apply -f -
kubectl --context kind-shipops get nodes
kubectl --context kind-shipops get storageclass
