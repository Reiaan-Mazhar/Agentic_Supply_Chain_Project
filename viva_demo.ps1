# Viva demo helper script (PowerShell)
# Paste and run from the project root folder or run this file.

$scriptDir = (Get-Location).Path
$python = Join-Path $scriptDir ".venv\Scripts\python.exe"

Write-Output "== Viva demo script starting =="
Write-Output "Working dir: $scriptDir"

# 1) Ensure venv python exists (if not, create venv and install deps — may take time)
if (-not (Test-Path $python)) {
  Write-Output "Virtualenv not found. Creating .venv and installing requirements (this may take several minutes)..."
  python -m venv .venv
  & .\.venv\Scripts\Activate.ps1
  & $python -m pip install --upgrade pip
  & $python -m pip install -r requirements.txt
} else {
  Write-Output "Using venv python: $python"
}

# 2) Ingest documents (build local vector DB)
Write-Output "`n== Running ingestion (ingest_data.py) =="
& $python ingest_data.py
if ($LASTEXITCODE -ne 0) { Write-Output "Ingest failed (exit $LASTEXITCODE)"; exit $LASTEXITCODE }

# 3) Start API (uvicorn) in background
Write-Output "`n== Starting API (uvicorn) in background =="
$uvicornProc = Start-Process -FilePath $python -ArgumentList '-m','uvicorn','main:app','--host','127.0.0.1','--port','8000' -NoNewWindow -PassThru
Start-Sleep -Seconds 3

# 4) Demo query to /chat
Write-Output "`n== Sending demo query to /chat =="
$body = @{ thread_id='demo'; message='What is the risk score for severity 9 and inventory 10?' } | ConvertTo-Json
try {
  $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/chat' -Method Post -ContentType 'application/json' -Body $body -ErrorAction Stop
  Write-Output "`n--- API response (object) ---"
  $resp | ConvertTo-Json -Depth 4 | Write-Output
} catch {
  Write-Output "API request failed: $_"
}

# 5) Run evaluation gate (CI mode) and print results
Write-Output "`n== Running evaluation gate (run_eval.py) =="
$env:CI = "true"
& $python run_eval.py
Write-Output "`nrun_eval exit code: $LASTEXITCODE"
if (Test-Path "eval_results.json") {
  Write-Output "`n--- eval_results.json ---"
  Get-Content eval_results.json -Raw
} else {
  Write-Output "No eval_results.json produced."
}

# 6) Print threshold config and small evidence files
Write-Output "`n--- eval_threshold_config.json ---"
if (Test-Path "eval_threshold_config.json") { Get-Content eval_threshold_config.json -Raw } else { Write-Output "Missing eval_threshold_config.json" }

Write-Output "`n--- Dockerfile ---"
Get-Content Dockerfile -Raw

Write-Output "`n--- docker-compose.yaml ---"
Get-Content docker-compose.yaml -Raw

# 7) Show persistence: local chroma_db contents (top files)
Write-Output "`n--- Persistence: chroma_db contents (top 20 files) ---"
if (Test-Path ".\chroma_db") {
  Get-ChildItem -Path .\chroma_db -Recurse -File | Select-Object -First 20 | ForEach-Object { Write-Output $_.FullName }
} else {
  Write-Output "No ./chroma_db folder found."
}

# 8) Stop API
Write-Output "`n== Stopping API =="
if ($uvicornProc -and $uvicornProc.Id) {
  try { Stop-Process -Id $uvicornProc.Id -Force; Write-Output "Stopped uvicorn (pid $($uvicornProc.Id))." } catch { Write-Output "Could not stop process: $_" }
} else {
  Write-Output "Could not find uvicorn process handle; check manually."
}

Write-Output "`n== Viva demo script complete =="
