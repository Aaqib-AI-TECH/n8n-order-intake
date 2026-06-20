#!/usr/bin/env bash
# Trigger the workflow with the sample order (bash / curl).
# Use the -test URL while the workflow is open and listening in the editor;
# use the production URL (without -test) once the workflow is activated.

curl -X POST "http://localhost:5678/webhook-test/order-intake" \
  -H "Content-Type: application/json" \
  -d @sample_payload.json

# Production (activated workflow):
# curl -X POST "http://localhost:5678/webhook/order-intake" \
#   -H "Content-Type: application/json" \
#   -d @sample_payload.json
