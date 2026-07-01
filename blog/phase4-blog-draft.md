# How We Cut 70 Seconds Off a TORCS Lap Using Rule-Based Physics and IBM Granite

*Team MDC Racing — Miami Dade College | IBM AI in Action Racing League 2026*

---

## 1. Who We Are

We are Louis Rodriguez and mfundora007, a two-person team from Miami Dade College (MDC) competing in the IBM AI in Action Racing League. Louis is a computer science student with a background in Python systems programming and data engineering; our teammate brings additional perspectives on experimentation workflow and telemetry strategy. Neither of us came into this project as racing engineers — we learned the physics on the fly, one crash at a time, and we think that learning arc is exactly what this competition is designed to produce.

Our GitHub repository is `LouisRodriguez12101815/ibmRacingLeague`. This post covers the full arc of the project: where we started, how we built our driver, how IBM Granite fit into the workflow, and what we are submitting.

---

## 2. What Is the IBM Racing League and What Are We Trying to Do

The IBM AI in Action Racing League challenges student teams to build an autonomous AI driver for TORCS (The Open Racing Car Simulator). Each team's driver competes on a single standing-start lap of the Corkscrew road course, driving the IBM F1 car. The judging criterion is simple: fastest clean lap wins — no pit stops, no multi-lap averages, no opponents to dodge.

Our goal is to get the IBM F1 car around Corkscrew as fast as possible without going off-track or accumulating damage. At the start of the project our car crawled around in 3 minutes 32 seconds. Our current best clean lap is **2 minutes 23 seconds**, and Bayesian modeling of our telemetry suggests a target of around **2 minutes 02–03 seconds** is achievable before submission day.

The gap to the publicly known fastest competitor (Darien Da Costa, Queen Mary University of London, approximately 1:23) is real and we are not going to pretend otherwise. But we believe our architecture and our data strategy put us on the right trajectory to close it.

---

## 3. Development Environment

Our stack is intentionally lean:

- **TORCS 1.3.4** (IBM Quick Start bundle) running on a Windows desktop with an RTX 3050 GPU. The IBM bundle uses the Simulated Car Racing (SCR) architecture: TORCS ships a built-in `scr_server` robot that opens a UDP socket on port 3001 and waits for an external Python client. Our driver is a Python UDP client — no C++ toolchain required.
- **Python 3.12** with only stdlib dependencies for the driver itself (`socket`, `sys`, `os`, `time`). `gym==0.26.2` is installed but the driver does not use the Gym interface; it communicates directly over UDP via `snakeoil3_gym.py`.
- **IBM Granite models via Ollama** — we run `granite4:tiny-h` (4.2 GB) and `granite4:350m-h` (366 MB) locally. Granite is integrated into our VSCode workflow through the **continue.dev** extension, which gives us an AI chat panel directly next to our code and telemetry files.
- **Zo Computer** — our remote Linux server, used for heavier Granite calls, running the Bayesian hyperparameter sweep (Optuna, 1000+ trials), SAC reinforcement learning training, and as a staging environment for experiments that would be too slow on the local laptop.
- **Two-PowerShell manual launch regime** — Window A runs TORCS in Quick Race mode; Window B runs the Python driver with flags for the current experiment. Simple, deterministic, and fast to iterate on.

---

## 4. How We Used IBM Granite

Granite is not in our real-time control loop. The IBM F1 car completes a lap in roughly 2.5 minutes; the TORCS physics tick fires every 22 ms. There is no practical way for an LLM to participate in that loop, nor would we want it to — every millisecond of Python overhead is a millisecond of delayed actuation.

Instead, Granite functions as our **offline strategy analyst**. Here is how the workflow actually looks:

**Telemetry review.** After every run we have a per-segment report: speed, peak steering angle, peak `trackPos`, time loss vs the previous best. We paste that report into the Granite chat panel and ask: "s09 peak `|trackPos|` is 0.87 and our braking window starts at 2380 m. Where should we move the brake trigger to recover the 0.5 s we are losing at hairpin entry?" Granite reads the numbers and suggests a physics-grounded starting point for the next run.

**Config generation.** Our most significant Granite result came from Run 081 analysis. We fed the full per-segment report and asked Granite to identify where lap time was being lost. Granite's response: the car already *exceeded* its hairpin speed targets (s09 averaged 56.2 km/h at a 53 km/h target; s13 averaged 58.2 km/h at a 55 km/h target). The bottleneck was not entry speed but **exit line quality** — narrow exit positions were forcing late throttle onto the following straights. Granite generated a new config (`segments_granite_v1.yaml`) with wider exit positions at s09 and s13, producing estimated 2–3 s of re-acceleration gain. This config is queued for tonight's live validation.

**Offline strategy analysis.** When we hit a plateau (Run 031 at 156 s was stuck for several sessions), we pasted our full run history into Granite and asked for a structured hypothesis ranking. Granite returned a prioritized list: resolve the s08 kink elevation hypothesis first, then refine the s09 late-apex line, then push straight targets. That order matched what the physics told us, which gave us confidence to commit to the s08 investigation rather than chasing marginal straight-speed gains.

This pattern — dense telemetry in, structured strategy out — is the right use of a language model in a real-time control problem. Granite earns its place by making our per-run decision-making faster and better-reasoned, not by touching the steering wheel.

---

## 5. Driver Architecture

`src/driver_baseline.py` is a rule-based controller with five primary subsystems:

**Segment-based speed targets.** The Corkscrew track is divided into 18 named segments stored in a YAML config file. Each segment has a `target_speed_kmh`, a kind (`straight` or `corner`), and a racing-line specification (`entry_pos`, `apex_pos`, `exit_pos` in `[-1, +1]` track-width units). The driver reads this file at startup; changing the config is the only thing needed to try a new strategy.

**Racing-line interpolation.** A steering law smoothly interpolates between entry, apex, and exit positions based on how far through the segment the car currently is. This means the car does not just aim at the centerline — it enters wide, cuts toward the apex, and exits wide, exploiting the full track width. Run 029 validated that the interpolator was working (peak `|trackPos|` rose to 0.82 on the best corners), and Runs 030–031 showed it translating into lap time.

**Lookahead brake physics.** The driver computes braking distance as `(v² − v_target²) / (2 × decel)` and triggers `brake = 1.0` when the car is that distance from the next corner's target speed. The deceleration constant (18 m/s² for the current configuration) comes from a dedicated brake calibration sprint in which we measured the IBM F1 car's actual deceleration under a full brake application: **22 m/s² mean, 25 m/s² peak**. Our earlier guess of 14 m/s² was 35% too conservative and was costing us seconds on every hairpin approach.

**PD steering with 3-sensor averaging (implemented 2026-04-28).** The original P-only steering law `(angle − trackPos × 0.5) / STEER_LOCK` had no derivative term and allowed oscillation near the centerline. We added a derivative term with `Kd = 0.10` and a weighted average of three track rangefinder sensors at −20°/0°/+20° to smooth the angle input. Mock testing confirmed: `kd = 0.10` reduced average `|trackPos|` from 0.291 to 0.243 across 10 laps. Both are controlled by CLI flags `--steer-kd 0.10` and `--no-sensor-avg`, so A/B testing is a single flag change.

**Trail braking (implemented 2026-04-28).** When the car simultaneously brakes and steers, the driver now reduces brake pressure proportional to steer angle: `trail_factor = max(0.4, 1.0 − |steer| × 0.6)`. This transfers weight more gradually to the front tires during braking in a corner, reducing the risk of rear snap at hairpin entry. Controlled by `--trail-brake` flag. Mock testing showed 0.06s improvement over 10 laps — marginal on its own but contributes to cleaner hairpin exits.

There is no neural network in the control loop. We considered Soft Actor-Critic reinforcement learning (our `scripts/train_sac.py` reached 1,500+ training episodes on Zo), but the SAC agent's success rate on completing a clean lap was below 1%, far too low to be submission-competitive on the current timeline. The physics-grounded rule-based approach is faster to iterate, easier to interpret, and currently faster on track.

---

## 6. Telemetry and Data Strategy

Our competitive moat is not a better algorithm — it is a richer dataset.

Every run is archived to `telemetry/runs/<timestamp>/` containing `frames.ndjson` (one JSON object per 22 ms tick), `manifest.json` (run metadata including git commit, driver flags, and notes), and a post-lap segment report. Every archive must pass `scripts/validate_run.py` against `telemetry/SCHEMA.md v0.2` before it is committed. The validator caught a real schema violation on Run 005 (post-race frames logged after `curLapTime` reset) that would have corrupted our baseline if it had made it into the dataset.

What we log that other teams likely do not: full `track[0..18]` proximity ray array, `wheelSpinVel[0..3]` for slip estimation, `z` (altitude) added specifically to test the s08 kink elevation hypothesis, controller decision metadata (which segment, which speed target, brake trigger state), and a segment-level smoothness score.

The elevation field paid off directly. The s08 kink at 1940–1960 m had produced 6+ consecutive DNFs despite repeated speed reductions. Plotting the `z` field from archived telemetry revealed a track crest at exactly 1940 m — a +5.33 mm rise over baseline, with a sharp −5 mm drop in the following 10 m. The crest unloads rear tires at the moment of peak lateral demand (steer 0.52–0.55, trackPos −0.80 to −0.84). The fix — reduce s08b from 83 to 78 km/h and hug the outside line before the crest — is implemented in `segments_elevation_informed.yaml` and is a targeted experiment for tonight.

The result: over **80 archived runs**, each fully labeled, forming a training dataset for Granite-assisted analysis and Bayesian hyperparameter search. When we want to know whether s08's grip problem is geometric or a weight-transfer crest, we do not guess — we have the altitude profile.

---

## 7. Key Results and Progression

The table below shows the major milestones from our first lap to the current best.

| Run | Date | Lap Time | Damages | Key Change |
|-----|------|----------|---------|------------|
| 001 | 2026-04-21 | 212.99 s (3:32.99) | 0 | First working driver — 55 km/h flat |
| 007 | 2026-04-22 | 170.57 s (2:50.57) | 41 | 80 km/h everywhere — fast but crashed |
| 008 | 2026-04-22 | 175.11 s (2:55.11) | 0 | 80 km/h + two slow zones — first clean sub-3:00 |
| 013 | 2026-04-22 | 165.67 s (2:45.67) | 0 | Segment YAML driver + lookahead braking |
| 023 | 2026-04-22 | 160.67 s (2:40.67) | 0 | Brake calibration applied — former submission anchor |
| 031 | 2026-04-24 | 156.59 s (2:36.59) | 0 | Racing-line interpolator + straight-speed push |
| 059 | 2026-04-26 | 145.25 s (2:25.25) | 0 | First AI-assisted candidate promoted |
| 063 | 2026-04-26 | 144.63 s (2:24.63) | 0 | AI section-B (s09 hairpin) specialization |
| 071 | 2026-04-26 | 143.31 s (2:23.31) | 0 | Straight-speed push — **current locked baseline** |
| *TBD* | 2026-04-28 | *130–128s target* | 0 | Bayesian + Granite + PD steering + trail braking |

**Overall improvement to date: −69.7 s (−32.7%) from Run 001 to Run 071.** The car went from a cautious 55 km/h crawl to a 115 km/h top speed with full-pedal braking into hairpins.

The three biggest single gains were: (1) the jump from 55 km/h to a speed-zoned 80 km/h target in Run 008 (−38 s); (2) the brake calibration sprint that unlocked correct lookahead distances (−5 s by Run 023); and (3) the racing-line interpolator paying out across Runs 029–031 and then the AI-candidate promotion cycle (Runs 059–071, −12.9 s). None of these were lucky — each was hypothesis-driven, measured against the previous anchor, and only promoted after a repeatability check within 0.1 s.

Analytical prediction for tonight's best candidate (mega_candidate): **130.2 s** — which would be a −13.1 s improvement over Run 071 in a single session, and would clear the sub-2:10 target.

---

## 8. Challenges and Lessons Learned

**The s08 kink at 1950 m.** There is a microsite on what our segment map labels as a straight where the car drifts toward the left barrier at any speed above ~95 km/h. Six consecutive run attempts between Runs 030 and 035 failed there in some form. The root cause was confirmed via elevation analysis — the real Corkscrew at Laguna Seca has a famous crest in this section, and IBM's track preserves it. A tire crossing a crest loses vertical load; the same lateral demand that was within traction limits on flat ground now exceeds the grip pool. Adding altitude logging to the telemetry schema confirmed a crest at 1940–1960 m. The practical fix is a narrow micro-zone with a lowered speed cap and an outside entry line to pre-load the tires before the crest.

**s09 and s13 hairpin exit lines.** The racing-line interpolator is powerful enough to pull the car past the track edge when the apex position is too aggressive and entry speed is too high. Runs 034 and 035 demonstrated this at s09 (peak `trackPos` +2.60 — the car cut across the inside kerb). The lesson: validate apex positions with a conservative entry speed before pushing the speed target, not simultaneously with it. We now treat corner line and corner speed as two independent experiments. Granite's exit-line analysis confirmed this — the bottleneck was never the corner speed, it was the exit width leaving room for throttle application.

**SAC reinforcement learning limitations.** We implemented a full SAC trainer on Zo and ran 1,500+ training episodes. The agent learned to steer but had a lap completion rate below 1%. Three root causes: (1) reward scale mismatch — the lap completion bonus (+1000) was 2000× larger than per-step reward (~0.5), causing Q-function explosion; (2) no gradient clipping, so any spike permanently corrupted the policy; (3) no diagnostic visibility. All three were fixed: rewards rescaled to 10–20× per-step magnitude, `clip_grad_norm_(max_norm=1.0)` added, 100-episode diagnostic prints implemented. Training is now stable. RL remains a long-term investment for this competition; the rule-based driver is the submission vehicle.

**Measurement before tuning.** Our biggest process lesson: the brake calibration sprint (measuring the IBM F1's real decel at 22 m/s² mean vs our assumed 14 m/s²) was more valuable than any single tuning run. Runs 016–018 failed because we were tuning against a wrong constant. Two hours of measurement saved us three sessions of empirical fumbling.

---

## 9. What Is Next

**Tonight's live validation (2026-04-28).** Six Bayesian and Granite-generated configs are queued for live TORCS runs in order of risk: C2 conservative → elevation-informed kink fix → Granite v1 exit lines → C1 Bayesian best → mega candidate (all combined) → C5 aggressive ceiling. Every run uses the new `--steer-kd 0.10 --trail-brake` flags. Analytical prediction for the mega candidate: **130.2 s**, clearing the sub-2:10 target and opening competitive range toward Darien Da Costa's 1:23.61.

**Gap to the leader.** Our analytical gap analysis shows 46.6 s remaining to Darien's pace. 64% of that gap (29.8 s) is on straights — the car needs to sustain 138–145 km/h instead of our current 103–135 km/h. 36% (16.8 s) is in corners, primarily the s09 hairpin where Darien likely takes 90 km/h to our 58 km/h. Closing the straight gap is mostly about trust in the Bayesian configs; closing the corner gap requires deeper racing-line work that may extend into Phase 5.

**Submission deadline: 2026-07-01.** We are targeting a Phase 5 dress rehearsal by June 25, with the final submission before June 28 to preserve a three-day buffer. The fastest-lap video (standing start, full-screen, university overlay for full duration) and team video (under 3 minutes, covering AI strategy and IBM SkillsBuild badges) will be recorded in Phase 5.

We started with a car that drove at 55 km/h and finished 3 minutes and 33 seconds later. We now have a car that takes corners at 85 km/h, brakes from 115 km/h in 60 meters, and completes a clean lap in 2 minutes 23 seconds. Tonight we find out if the Bayesian sweep and Granite analysis close another 13 seconds. The physics say there is more time on this track, and we intend to find it.

---

*Team MDC Racing — Louis Rodriguez & mfundora007, Miami Dade College*  
*IBM AI in Action Racing League | Corkscrew Track | IBM F1 Car*  
*Repository: `LouisRodriguez12101815/ibmRacingLeague` | IBM Granite via Ollama + continue.dev*

<!-- updated 2026-04-28 — reflects PD steering done, trail braking done, Bayesian 1000+ trials done, elevation analysis done, Granite v1 config done -->
