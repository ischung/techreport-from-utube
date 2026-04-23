#!/usr/bin/env bash
#
# scripts/smoke.sh — staging smoke test (issue #6, CI-6)
#
# Verifies that the stack brought up by `docker compose up -d` is actually
# serving traffic. Called from .github/workflows/deploy-staging.yml and
# usable locally: `./scripts/smoke.sh`.
#
# Exit codes:
#   0  all probes passed
#   1  at least one probe failed (the caller is responsible for tearing down)
#
# Configurable via env:
#   FRONTEND_URL  (default: http://localhost/)
#   BACKEND_URL   (default: http://localhost:8000/)
#   MAX_ATTEMPTS  (default: 6)
#   SLEEP_SECONDS (default: 5)

set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost/}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8000/}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-6}"
SLEEP_SECONDS="${SLEEP_SECONDS:-5}"

log() { printf '[smoke] %s\n' "$*"; }

probe() {
  local name="$1" url="$2" want_body_check="${3:-no}"
  local attempt
  for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
    if [[ "$want_body_check" == "yes" ]]; then
      if curl -fsS -o /tmp/smoke-body.$$ "$url"; then
        log "✓ ${name} ok (attempt ${attempt})"
        log "  body: $(head -c 200 /tmp/smoke-body.$$)"
        rm -f /tmp/smoke-body.$$
        return 0
      fi
    else
      local code
      code=$(curl -fsSI -o /dev/null -w '%{http_code}' "$url" || echo "000")
      if [[ "$code" == "200" ]]; then
        log "✓ ${name} ok (HTTP 200, attempt ${attempt})"
        return 0
      fi
      log "  ${name} not ready yet (attempt ${attempt}, HTTP ${code})"
    fi
    sleep "$SLEEP_SECONDS"
  done
  log "✗ ${name} failed after ${MAX_ATTEMPTS} attempts"
  return 1
}

log "Frontend target: ${FRONTEND_URL}"
log "Backend  target: ${BACKEND_URL}"

FAIL=0
probe "backend" "${BACKEND_URL}" "yes"     || FAIL=1
probe "frontend" "${FRONTEND_URL}" "no"    || FAIL=1

if ((FAIL == 1)); then
  log "One or more probes failed."
  exit 1
fi

log "All probes passed."
