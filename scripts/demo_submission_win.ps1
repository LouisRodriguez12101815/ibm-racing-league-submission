# demo_submission_win.ps1 -- run the baseline controller on Windows.
#
# Prereq: TORCS is running with:
#   Race -> Quick Race -> Configure Race
#   Track: road/corkscrew
#   Driver: scr_server 1 only
#   Laps: 1
#   New Race (TORCS will appear stuck / Not Responding until Python connects)
#
# Usage (from repo root):
#   pwsh -File .\scripts\demo_submission_win.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$SegmentsFile = "telemetry\segments_baseline_current.yaml"
$Driver = "src\driver_baseline.py"

if (-not (Test-Path $SegmentsFile)) {
    Write-Error "Missing $SegmentsFile. Run from repo root."
    exit 1
}
if (-not (Test-Path $Driver)) {
    Write-Error "Missing $Driver. Run from repo root."
    exit 1
}

$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "========================================"
Write-Host "  IBM AI Racing League - Submission lap (Windows)"
Write-Host "========================================"
Write-Host "Segments: $SegmentsFile"
Write-Host "Driver:   $Driver"
Write-Host ""
Write-Host "TORCS SETUP CHECKLIST:"
Write-Host "  1) Launch C:\torcs\torcs\wtorcs.exe"
Write-Host "  2) Race -> Quick Race -> Configure Race"
Write-Host "  3) Track: road/corkscrew | Driver: scr_server 1 | Laps: 1"
Write-Host "  4) New Race, wait for TORCS to appear 'Not Responding'"
Write-Host ""

Read-Host "Press ENTER when TORCS is waiting for the driver"

Write-Host ""
Write-Host "Connecting driver..."
Write-Host ""

python $Driver `
    --segments $SegmentsFile `
    --full-pedal-brake `
    --lookahead 150 `
    --lookahead-decel 9.0 `
    --laps 1 `
    --notes "submission run"

Write-Host ""
Write-Host "Done. Latest run written under telemetry\runs\"
Write-Host "Verify clean lap with: python scripts\post_lap_verify.py"
