# Current submission baseline

**Status:** LOCKED (promoted)

## Submitted lap (recorded on video)

- **Submission run 2026-06-30T22-53-33:** `143.96 s` (`02:23.96`), damages 0, 1 lap completed
- Video: https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-lap-corkscrew-2-23-96.mp4
- Telemetry archive: `telemetry/runs/2026-06-30T22-53-33/`

## Prior best clean laps (repeatable)

- **Run 071:** `143.306 s` (`02:23.32`), top speed 121 km/h, damages 0, no off-tracks
- **Run 072 (repeat):** `143.326 s` (`02:23.32`), top speed 121 km/h, damages 0, no off-tracks

**Config:** `telemetry/segments_baseline_current.yaml` (source: `telemetry/segments_ai_candidate_straight_push.yaml`)

## Why this is the locked baseline

- Faster than prior locked baseline (`143.906 s`) by ~0.58–0.60 s.
- Two consecutive clean runs in a tight band (20 ms spread).
- `post_lap.md` flags only one near-edge watch item (s01 peak |trackPos| 0.973), with no off-track excursions.

## Practical guidance

Use this baseline for all future experiments. Create candidate configs as copies and apply surgical deltas by section.

Driver command:

```powershell
python src\driver_baseline.py --segments telemetry\segments_baseline_current.yaml --full-pedal-brake --lookahead 150 --lookahead-decel 9.0 --notes "Run XXX baseline"
```
