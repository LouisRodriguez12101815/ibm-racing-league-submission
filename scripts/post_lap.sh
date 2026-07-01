#!/usr/bin/env bash
set -euo pipefail

# post_lap.sh -- standardized post-lap analysis (macOS/Linux)
# Usage:
#   ./scripts/post_lap.sh
#   ./scripts/post_lap.sh --segments telemetry/segments_baseline_current.yaml
#
# Runs:
#   1) scripts/validate_run.py
#   2) scripts/find_offtracks.py
#   3) scripts/segment_report.py
#   4) scripts/post_lap_review.py

SEGMENTS="telemetry/segments.yaml"
BASELINE_RUN=""
BASELINE_SEGMENTS="telemetry/segments_baseline_current.yaml"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --segments)
      SEGMENTS="$2"; shift 2 ;;
    --baseline-run)
      BASELINE_RUN="$2"; shift 2 ;;
    --baseline-segments)
      BASELINE_SEGMENTS="$2"; shift 2 ;;
    -h|--help)
      sed -n '1,120p' "$0"; exit 0 ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: python not found (set PYTHON_BIN or install python3)." >&2
  exit 1
fi

export PYTHONIOENCODING="utf-8"

if [[ ! -d telemetry/runs ]]; then
  echo "ERROR: telemetry/runs/ not found. Run from ibmRacingLeague/ directory." >&2
  exit 1
fi

RUN_DIR_NAME="$(ls -1t telemetry/runs 2>/dev/null | head -n 1 || true)"
if [[ -z "$RUN_DIR_NAME" ]]; then
  echo "ERROR: no run archives found under telemetry/runs/." >&2
  exit 1
fi

RUN_DIR="telemetry/runs/${RUN_DIR_NAME}"

echo ""
echo "========================================"
echo "  POST-LAP ANALYSIS -- ${RUN_DIR_NAME}"
echo "========================================"
echo "Segments: ${SEGMENTS}"
if [[ -n "$BASELINE_RUN" ]]; then
  echo "Baseline run: ${BASELINE_RUN}"
fi

echo ""
echo "[1/4] Validating schema..."
"$PYTHON_BIN" scripts/validate_run.py "$RUN_DIR" --segments-file telemetry/segments.txt

echo ""
echo "[2/4] Scanning for off-tracks..."
"$PYTHON_BIN" scripts/find_offtracks.py "$RUN_DIR" --threshold 1.0

echo ""
echo "[3/4] Generating segment report..."
"$PYTHON_BIN" scripts/segment_report.py "$RUN_DIR" --segments "$SEGMENTS"

echo ""
echo "[4/4] Generating post-lap engineering review..."
review_args=(scripts/post_lap_review.py "$RUN_DIR" --segments "$SEGMENTS")
if [[ -n "$BASELINE_RUN" ]]; then
  review_args+=(--baseline-run "telemetry/runs/$BASELINE_RUN" --baseline-segments "$BASELINE_SEGMENTS")
fi
"$PYTHON_BIN" "${review_args[@]}"

echo ""
echo "========================================"
echo "  Done. Review: ${RUN_DIR}/post_lap.md"
echo "========================================"
echo ""