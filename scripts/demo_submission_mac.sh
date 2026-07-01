#!/usr/bin/env bash
set -euo pipefail

# demo_submission_mac.sh -- run the current baseline controller on macOS (Wine)
#
# TORCS must already be running with:
#   Race -> Quick Race -> Configure Race
#   Track: road/corkscrew
#   Driver: scr_server 1 only
#   Laps: 1
#   New Race (TORCS will appear stuck / Not Responding until the Python client connects)
#
# Usage (from ibmRacingLeague/ directory):
#   ./scripts/demo_submission_mac.sh

SEGMENTS_FILE="telemetry/segments_baseline_current.yaml"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: python not found (set PYTHON_BIN or install python3)." >&2
  exit 1
fi

if [[ ! -f "$SEGMENTS_FILE" ]]; then
  echo "ERROR: $SEGMENTS_FILE not found. Run from ibmRacingLeague/ directory." >&2
  exit 1
fi

if [[ ! -f "src/driver_baseline.py" ]]; then
  echo "ERROR: src/driver_baseline.py not found. Run from ibmRacingLeague/ directory." >&2
  exit 1
fi

export PYTHONIOENCODING="utf-8"

echo ""
echo "========================================"
echo "  IBM AI Racing League — Submission lap (Mac/Wine)"
echo "========================================"
echo "Segments: $SEGMENTS_FILE"
echo "Driver: src/driver_baseline.py"
echo ""
echo "TORCS SETUP:"
echo "  1) wine wtorcs.exe"
echo "  2) Race -> Quick Race -> Configure Race"
echo "  3) Track: road/corkscrew | Driver: scr_server 1 | Laps: 1"
echo "  4) New Race, wait for TORCS to appear stuck/not responding"
echo ""

read -r -p "Press ENTER when TORCS is waiting for the driver..." _

echo ""
echo "Connecting driver..."
echo "  $PYTHON_BIN src/driver_baseline.py --segments $SEGMENTS_FILE --full-pedal-brake --lookahead 150 --lookahead-decel 9.0 --laps 1 --notes \"submission run\""
echo ""

"$PYTHON_BIN" src/driver_baseline.py \
  --segments "$SEGMENTS_FILE" \
  --full-pedal-brake \
  --lookahead 150 \
  --lookahead-decel 9.0 \
  --laps 1 \
  --notes "submission run"

echo ""
echo "Done. Next: ./scripts/post_lap.sh --segments $SEGMENTS_FILE"