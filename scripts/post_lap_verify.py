#!/usr/bin/env python3
"""Quick post-lap verifier.

Reads the newest telemetry run and prints:
  - Run ID
  - Lap time (from manifest.json if present)
  - Damage count
  - Frame count

Usage:
    python scripts/post_lap_verify.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    runs_dir = repo_root / "telemetry" / "runs"
    if not runs_dir.exists():
        print(f"ERROR: no runs directory at {runs_dir}", file=sys.stderr)
        return 1

    runs = sorted([p for p in runs_dir.iterdir() if p.is_dir()])
    if not runs:
        print(f"ERROR: no runs found in {runs_dir}", file=sys.stderr)
        return 1

    latest = runs[-1]
    manifest_path = latest / "manifest.json"
    frames_path = latest / "frames.ndjson"

    print("=" * 60)
    print(f"Latest run: {latest.name}")
    print("=" * 60)

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"WARN: could not parse manifest.json: {exc}")
            manifest = {}
        for key in ("run_id", "notes", "lap_time_s", "lap_time", "damage",
                    "damages", "clean", "status", "distance_m", "started_at",
                    "finished_at"):
            if key in manifest:
                print(f"  {key:14s}: {manifest[key]}")

    frame_count = 0
    max_damage = 0
    last_lap_time = None
    if frames_path.exists():
        with frames_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                frame_count += 1
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                dmg = row.get("damage")
                if isinstance(dmg, (int, float)) and dmg > max_damage:
                    max_damage = dmg
                lt = row.get("lastLapTime") or row.get("curLapTime")
                if isinstance(lt, (int, float)) and lt > 0:
                    last_lap_time = lt

    print(f"  frames        : {frame_count}")
    print(f"  peak damage   : {max_damage}")
    if last_lap_time is not None:
        m = int(last_lap_time // 60)
        s = last_lap_time - 60 * m
        print(f"  last lap time : {last_lap_time:.3f}s ({m}:{s:06.3f})")

    verdict = "CLEAN" if max_damage == 0 else f"DAMAGED ({max_damage})"
    print()
    print(f"VERDICT: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
