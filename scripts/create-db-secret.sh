#!/usr/bin/env bash
set -euo pipefail
# Generates credentials only in a temporary permission-restricted file.
# Never commits or prints the password.
umask 077
if kubectl --context kind-shipops -n shipops get secret shipops-db-auth >/dev/null 2>&1; then
  echo "Existing secret shipops-db-auth found; preserving the database password."
  exit 0
fi
secret_file=$(mktemp)
trap 'rm -f "$secret_file"' EXIT
printf '%s' "$(openssl rand -hex 24)" > "$secret_file"
kubectl --context kind-shipops -n shipops create secret generic shipops-db-auth   --from-literal=username=shipops   --from-file=password="$secret_file"
echo "Database authentication secret created (password not printed)."
