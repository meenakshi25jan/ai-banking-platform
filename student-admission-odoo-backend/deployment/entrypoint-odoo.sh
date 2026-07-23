#!/bin/bash
set -euo pipefail

# Database connection (avoid clashing with shell USER)
DB_HOST="${HOST:-db}"
DB_PORT="${PORT:-5432}"
DB_USER="${ODOO_DB_USER:-odoo}"
DB_PASSWORD="${PASSWORD:-odoo}"
DATABASE="${ODOO_DATABASE:-student_admission}"
INIT_MARKER="/var/lib/odoo/.${DATABASE}_initialized"

echo "==> [Odoo] Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
for i in $(seq 1 60); do
  if PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -c '\q' 2>/dev/null; then
    echo "==> [Odoo] PostgreSQL is ready."
    break
  fi
  if [ "$i" -eq 60 ]; then
    echo "ERROR: PostgreSQL not available after 120 seconds."
    exit 1
  fi
  sleep 2
done

if [ ! -f "${INIT_MARKER}" ]; then
  echo "==> [Odoo] First-time setup for database: ${DATABASE}"

  DB_EXISTS=$(PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${DATABASE}'" 2>/dev/null || echo "")

  if [ "${DB_EXISTS}" != "1" ]; then
    echo "==> [Odoo] Creating database ${DATABASE}..."
    PGPASSWORD="${DB_PASSWORD}" createdb -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" "${DATABASE}"
  fi

  echo "==> [Odoo] Installing modules: base, student_admission (with demo data)..."
  odoo -c /etc/odoo/odoo.conf \
    -d "${DATABASE}" \
    -i base,student_admission \
    --without-demo=False \
    --stop-after-init \
    --db_host="${DB_HOST}" \
    --db_port="${DB_PORT}" \
    --db_user="${DB_USER}" \
    --db_password="${DB_PASSWORD}"

  touch "${INIT_MARKER}"
  echo "==> [Odoo] Database initialization complete."
else
  echo "==> [Odoo] Database already initialized (${DATABASE})."
fi

echo "==> [Odoo] Starting server on port 8069..."
exec odoo -c /etc/odoo/odoo.conf \
  --db_host="${DB_HOST}" \
  --db_port="${DB_PORT}" \
  --db_user="${DB_USER}" \
  --db_password="${DB_PASSWORD}" \
  "$@"
