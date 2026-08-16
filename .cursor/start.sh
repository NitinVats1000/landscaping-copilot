#!/usr/bin/env bash
set -euo pipefail

PG_VERSION="$(ls /etc/postgresql/ 2>/dev/null | sort -rn | head -1)"
if [[ -z "${PG_VERSION}" ]]; then
  echo "PostgreSQL is not installed." >&2
  exit 1
fi

if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
  sudo mkdir -p /var/run/postgresql
  sudo chown postgres:postgres /var/run/postgresql
  if command -v pg_ctlcluster >/dev/null 2>&1; then
    sudo pg_ctlcluster "${PG_VERSION}" main start
  else
    sudo -u postgres "/usr/lib/postgresql/${PG_VERSION}/bin/pg_ctl" \
      -D "/var/lib/postgresql/${PG_VERSION}/main" \
      -l /tmp/postgresql.log start
  fi
fi

sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='copilot'" | grep -q 1 \
  || sudo -u postgres psql -c "CREATE USER copilot WITH PASSWORD 'copilot_dev_pw';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='copilot'" | grep -q 1 \
  || sudo -u postgres psql -c "CREATE DATABASE copilot OWNER copilot;"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT/docs"
uv run alembic upgrade head
