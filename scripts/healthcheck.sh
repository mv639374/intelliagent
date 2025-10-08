#!/bin/bash
# scripts/healthcheck.sh

# This script checks the health of the backend service.
# It requires the API to expose a /api/health endpoint that returns a 200 status code.

set -eo pipefail

HOST=${1:-"localhost"}
PORT=${2:-"8000"}
HEALTH_ENDPOINT="/api/health"
MAX_ATTEMPTS=10
SLEEP_DURATION=3

echo "Attempting to connect to http://${HOST}:${PORT}${HEALTH_ENDPOINT}"

for ((i=1; i<=MAX_ATTEMPTS; i++)); do
    # Use curl to check the health endpoint
    # -s for silent, -o /dev/null to discard output, -w "%{http_code}" to get status
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://${HOST}:${PORT}${HEALTH_ENDPOINT}")

    if [[ "$STATUS_CODE" -eq 200 ]]; then
        echo "✅ Health check successful! Service is up."
        exit 0
    else
        echo "Attempt $i/$MAX_ATTEMPTS: Failed with status code $STATUS_CODE. Retrying in $SLEEP_DURATION seconds..."
        sleep $SLEEP_DURATION
    fi
done

echo "❌ Health check failed after $MAX_ATTEMPTS attempts. Service is unreachable."
exit 1
