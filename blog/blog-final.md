# How We Cut 70 Seconds Off a TORCS Lap Using Rule-Based Physics and IBM Granite

*Team MDC Racing — Miami Dade College | IBM AI in Action Racing League 2026*

---

## 1. Who We Are

We are Louis Rodriguez and our teammate mfundora007, a two-person team from Miami Dade College (MDC) competing in the IBM AI in Action Racing League. Louis is a computer science student with a background in Python systems programming and data engineering. Neither of us came into this project as racing engineers — we learned the physics on the fly, one crash at a time, and that learning arc is exactly what this competition is designed to produce.

Our GitHub repository: [LouisRodriguez12101815/ibmRacingLeague](https://github.com/LouisRodriguez12101815/ibmRacingLeague)

---

## 2. What Is the IBM Racing League and What Are We Trying to Do

The IBM AI in Action Racing League challenges student teams to build an autonomous AI driver for TORCS (The Open Racing Car Simulator). Each team's driver competes on a single standing-start lap of the Corkscrew road course, driving the IBM F1 car. The judging criterion is simple: fastest clean lap wins.

Our goal was to get the IBM F1 car around Corkscrew as fast as possible without going off-track or accumulating damage. At the start of the project our car crawled around in 3 minutes 32 seconds. Our submitted best clean lap is **2 minutes 23 seconds (143.306s)** — a 70-second improvement over our starting point.

---

## 3. Development Environment

Our stack is intentionally lean:

- **TORCS 1.3.4** (IBM Quick Start bundle) running on a Windows desktop. The IBM bundle uses the SCR architecture: TORCS ships a built-in `scr_server` robot that opens a UDP socket on port 3001 and waits for an external Python client.
- **Python 3.12** with only stdlib dependencies for the driver itself (`socket`, `sys`, `os`, `time`).
- **IBM Granite models via Ollama** — we run `granite4:tiny-h` and `granite4:350m-h` locally, integrated into our VSCode workflow through the **continue.dev** extension.
- **Remote Linux server (Zo Computer)** — used for Bayesian hyperparameter sweeps (Optuna, 1000+ trials), SAC reinforcement learning training, and heavier Granite calls.

---

## 4. How We Used IBM Granite

Granite is not in our real-time control loop. Instead, Granite functions as our **offline strategy analyst**.

**Telemetry review.** After every run we paste a per-segment report into the Granite chat panel and ask physics-grounded questions: where should we move the brake trigger to recover the 0.5s we are losing at hairpin entry?

**Config generation.** Our most significant Granite result came from Run 081 analysis. Granite identified that the bottleneck was not entry speed but **exit line quality** — narrow exit positions were forcing late throttle onto the following straights. Granite generated a new config (`segments_granite_v1.yaml`) with wider exit positions at s09 and s13.

**Offline strategy analysis.** When we hit a plateau at Run 031 (156s), we pasted our full run history into Granite and asked for a structured hypothesis ranking. Granite returned a prioritized list that matched what the physics told us — which gave us confidence to commit to the s08 investigation rather than chasing marginal gains.

This pattern — dense telemetry in, structured strategy out — is the right use of a language model in a real-time control problem.

---

## 5. Driver Architecture

`src/driver_baseline.py` is a rule-based controller with five primary subsystems:

**Segment-based speed targets.** The Corkscrew track is divided into 18 named segments stored in a YAML config file. Each segment has a `target_speed_kmh`, a kind (`straight` or `corner`), and a racing-line specification (`entry_pos`, `apex_pos`, `exit_pos`).

**Racing-line interpolation.** A steering law smoothly interpolates between entry, apex, and exit positions — the car enters wide, cuts toward the apex, and exits wide, exploiting the full track width.

**Lookahead brake physics.** The driver computes braking distance as `(v² − v_target²) / (2 × decel)` and triggers `brake = 1.0` when the car is that distance from the next corner's target speed.

**PD steering with 3-sensor averaging.** A derivative term (`Kd = 0.10`) and weighted average of three track rangefinder sensors at −20°/0°/+20° reduce oscillation and improve tracking accuracy.

**Trail braking.** When the car simultaneously brakes and steers, brake pressure is reduced proportional to steer angle, transferring weight more gradually to the front tires.

There is no neural network in the control loop. We implemented full SAC reinforcement learning (1,500+ training episodes) but the rule-based driver is faster to iterate, easier to interpret, and currently faster on track.

---

## 6. Telemetry and Data Strategy

Every run is archived to `telemetry/runs/<timestamp>/` containing `frames.ndjson` (one JSON object per 22ms tick), `manifest.json` (run metadata), and a post-lap segment report. Every archive passes `scripts/validate_run.py` against SCHEMA v0.2.

Over **80 archived runs**, each fully labeled, form a training dataset for Granite-assisted analysis and Bayesian hyperparameter search.

---

## 7. Key Results and Progression

| Run | Date | Lap Time | Key Change |
|-----|------|----------|------------|
| 001 | 2026-04-21 | 3:32.99 | First working driver — 55 km/h flat |
| 008 | 2026-04-22 | 2:55.11 | 80 km/h + slow zones — first clean sub-3:00 |
| 013 | 2026-04-22 | 2:45.67 | Segment YAML driver + lookahead braking |
| 031 | 2026-04-24 | 2:36.59 | Racing-line interpolator |
| 059 | 2026-04-26 | 2:25.25 | First AI-assisted candidate promoted |
| **071** | **2026-04-26** | **2:23.31 ✅** | **Straight-speed push — locked submission baseline** |

**Overall improvement: −69.7s (−32.7%) from Run 001 to Run 071.**

---

## 8. Challenges and Lessons Learned

**The s08 kink.** Six consecutive DNFs at 1950m were resolved by adding altitude logging — revealing a track crest that unloads rear tires at the moment of peak lateral demand. The fix: a micro-zone with a lowered speed cap and outside entry line.

**Measurement before tuning.** A brake calibration sprint measuring the IBM F1's real deceleration (22 m/s² mean vs our assumed 14 m/s²) was worth more than any single tuning run.

**SAC RL limitations.** Our SAC agent learned to steer but had a lap completion rate below 1% due to reward scale mismatch and missing gradient clipping. Both were fixed; RL remains a long-term investment.

---

## 9. Submission Deliverables

- **Fastest lap video:** [LINK — upload to Google Drive and paste here]
- **Team video:** [LINK — upload to Google Drive and paste here]
- **GitHub repo:** https://github.com/LouisRodriguez12101815/ibmRacingLeague
- **IBM SkillsBuild badges:** [LINK — Google Slides deck]
- **Car livery:** MDC Racing F1 livery (deep royal blue, gold, IBM AI branding) — [LINK to Google Drive]

---

*Team MDC Racing — Louis Rodriguez & mfundora007, Miami Dade College*
*IBM AI in Action Racing League | Corkscrew Track | IBM F1 Car*
*Repository: [LouisRodriguez12101815/ibmRacingLeague](https://github.com/LouisRodriguez12101815/ibmRacingLeague) | IBM Granite via Ollama + continue.dev*
