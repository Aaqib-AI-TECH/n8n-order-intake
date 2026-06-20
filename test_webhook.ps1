# Trigger the workflow with the sample order (PowerShell, Windows).
#
# While editing the workflow in n8n, click "Listen for test event" on the
# webhook node first, then use the -test URL below. Once the workflow is
# ACTIVE (toggle top-right), use the production URL (without -test).

# --- Test URL (workflow open in the editor, listening) ---
$body = Get-Content -Raw .\sample_payload.json
Invoke-RestMethod -Method Post `
  -Uri "http://localhost:5678/webhook-test/order-intake" `
  -ContentType "application/json" `
  -Body $body

# --- Production URL (workflow activated) ---
# Invoke-RestMethod -Method Post `
#   -Uri "http://localhost:5678/webhook/order-intake" `
#   -ContentType "application/json" `
#   -Body $body
