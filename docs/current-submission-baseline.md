# Current submission baseline

**Status:** LOCKED (promoted)

## Best clean lap (repeatable)

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
