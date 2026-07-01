# From 3:32 to 2:23.96 — How FINN-ISH LINE Built an IBM AI Racing League Driver
*Team FINN-ISH LINE — Miami Dade College · IBM AI Racing League 2026*
When we started this project, our TORCS car crawled around Corkscrew in 3 minutes and 32 seconds. On submission day, it runs a clean, zero-damage lap in **2 minutes 23.96 seconds** — reproducible from the same command, from the same repo, on any machine with TORCS installed.
This is how we got there, what IBM Granite and IBM SkillsBuild had to do with it, and what we're actually submitting.
---

## Who we are

We are Louis Rodriguez, Daniel Pino, and Javier Perez-Hickman — the FINN-ISH LINE team from Miami Dade College's **AI Models** course. None of us started this project as racing engineers. We learned the physics on the fly, one off-track excursion at a time, and we think that learning arc is exactly what the IBM AI Racing League is designed to produce.

Our submission repo is public: [github.com/LouisRodriguez12101815/ibm-racing-league-submission](https://github.com/LouisRodriguez12101815/ibm-racing-league-submission)

---

## What the challenge asks

The IBM AI Racing League tasks student teams with building an autonomous AI driver for TORCS — The Open Racing Car Simulator. Each team's driver competes on a single **standing-start** lap of the **Corkscrew** road course in the IBM F1 car. Judging is straightforward: fastest clean lap wins. No pit stops. No multi-lap averaging. No opponents to dodge. Just a single flying lap and the physics.

Our goal was — and is — to get the IBM F1 car around Corkscrew as fast as possible without going off-track or accumulating damage.

---

## The stack

Our stack is intentionally lean, because the SCR (Simulated Car Racing) protocol makes it possible to be lean:

- **TORCS 1.3.4** running natively on Windows with an RTX 3050. TORCS ships a built-in `scr_server` robot that opens a UDP socket on port 3001 and waits for an external client — so we don't need a C++ toolchain.
- **Python 3.12** with only stdlib in the control loop. The driver connects to `scr_server` over UDP via a lightly modified `snakeoil3_gym.py` client.
- **IBM Granite models via Ollama** — we run `granite4:tiny-h` (4.2 GB) and `granite4:350m-h` (366 MB) locally, integrated into VS Code through the [Continue](https://continue.dev) extension. Granite is our offline strategy analyst, not a real-time controller. More on that below.
- **Two-terminal launch regime** — one window runs TORCS in Quick Race mode with `scr_server 1` as the sole driver on Corkscrew, 1 lap. A second window runs `scripts/demo_submission_win.ps1` (or `.sh` on Mac/Wine), which invokes the Python controller with the current experiment flags.

That's it. No cloud dependency in the control loop, no custom simulator build, no proprietary tooling.

---

## The driver architecture

`src/driver_baseline.py` is a rule-based controller with five subsystems:

1. **Segment-based speed targets.** Corkscrew is divided into 18 named segments in `telemetry/segments_baseline_current.yaml`. Each segment has a `target_speed_kmh`, a kind (straight or corner), and a racing-line specification (`entry_pos`, `apex_pos`, `exit_pos` in `[-1, +1]` track-width units). Change the YAML → change the strategy. No code changes needed to iterate.

2. **Racing-line interpolation.** A steering PD controller drives the car toward `target_track_pos_for(distFromStart)`, which linearly interpolates entry → apex → exit across each segment.

3. **Lookahead brake controller.** Given assumed deceleration (we use 9.0 m/s²) and a lookahead window (150 m), the controller pre-computes brake points from physics rather than reacting to overshoot. This one change is worth roughly 15 seconds of lap time on its own.

4. **Sensor smoothing.** The heading angle uses a weighted average of three track rangefinder rays (−20°, 0°, +20°, with the centre ray double-weighted) to suppress high-frequency noise on the straights.

5. **Structured telemetry logging.** Every run writes an NDJSON stream of per-tick state (`frames.ndjson`) plus a `manifest.json` with lap time, damage, and stop reason. This is the single most valuable engineering investment we made — it's what makes objective before/after comparison possible.

---

## How IBM Granite fits

Granite is **not** in our real-time control loop. Corkscrew takes roughly 2 minutes 24 seconds; TORCS physics ticks every 22 ms. There is no practical way for an LLM to participate in that loop, and even if there were, we wouldn't want it to — every millisecond of Python overhead is a millisecond of delayed actuation.

Instead, Granite is our **offline strategy analyst**. Three concrete uses:

**Telemetry review.** After every run we produce a per-segment report: speed, peak steering angle, peak `trackPos`, time loss vs the previous best. We paste that report into the Granite chat panel and ask focused questions like: "s09 peak `|trackPos|` is 0.87 and our braking window starts at 2380 m. Where should we move the brake trigger to recover the 0.5s we're losing at hairpin entry?" Granite reads the numbers and suggests a physics-grounded starting point.

**Config generation.** Our most impactful Granite result came from a run where we thought we needed more entry speed. We fed Granite the per-segment report and asked where lap time was being lost. Its response: we were already exceeding hairpin entry-speed targets — the bottleneck was **exit line quality**. Narrow exit positions were forcing late throttle onto the following straights. Granite generated a new YAML with wider exit positions at the identified segments, projecting 2–3 seconds of re-acceleration gain.

**Plateau-breaking hypothesis ranking.** When we hit a plateau, we pasted our full run history into Granite and asked for a prioritized hypothesis list. The ordering matched what the physics told us, giving us confidence to commit to one investigation instead of chasing marginal straight-line gains.

The pattern — dense telemetry in, structured strategy out — is the right use of a language model in a real-time control problem.

---

## How IBM SkillsBuild fits

The SkillsBuild badge track gave every member of FINN-ISH LINE shared vocabulary for the tradeoffs we were about to make.

The single most important thing SkillsBuild did for our project was convince us to ship a **deterministic controller first**. There is a persistent temptation in RL-adjacent problems to reach for reinforcement learning immediately. SkillsBuild content on sample efficiency, generalization, and the practicality of controllable local models framed the tradeoff clearly: for a single-lap, single-track, single-car problem with a physics simulator we can inspect, rule-based control is faster to iterate, easier to reason about, and produces evidence we can hand to a judge.

That framing is why we have a clean, reproducible 143.96s lap on submission day instead of a half-trained SAC policy.

---

## Reproducing our submission lap

The submission lap is reproducible from a fresh checkout. On Windows:

```
git clone https://github.com/LouisRodriguez12101815/ibm-racing-league-submission
cd ibm-racing-league-submission

# In one window: launch C:\torcs\torcs\wtorcs.exe
# Race -> Quick Race -> Configure Race
# Track: road/corkscrew | Driver: scr_server 1 | Laps: 1
# New Race (TORCS will show 'Not Responding' — this is correct)

# In another window:
.\scripts\demo_submission_win.ps1
# Press ENTER when TORCS is at the 'Not Responding' state
```

The Mac/Wine version (`scripts/demo_submission_mac.sh`) runs the same command with the same segments YAML and produces the same lap.

Verify the run:

```
python scripts\post_lap_verify.py
```

You want `VERDICT: CLEAN` and a lap time near **143.96s**.

---

## What we're submitting

- **Fastest lap video:** [`mdc-racing-lap-corkscrew-2-23-96.mp4`](https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-lap-corkscrew-2-23-96.mp4) — standing start, single lap, 143.96s clean, 0 damage.
- **Livery:** [`mdc_racing_livery.jpg`](https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc_racing_livery.jpg) — deep royal blue, gold accents, IBM AI branding, MDC identifier.
- **Team video:** linked from the submission packet.
- **Repo:** [github.com/LouisRodriguez12101815/ibm-racing-league-submission](https://github.com/LouisRodriguez12101815/ibm-racing-league-submission)

---

## What we'd do differently with more time

Three things:

1. **Ship the Granite-generated wider-exit config live.** We have `segments_granite_v1.yaml` queued but chose the more heavily validated `segments_baseline_current.yaml` for submission-day certainty. With a longer runway we would run 20 back-to-back validation laps on the Granite config and lock whichever ran a tighter time spread.

2. **Introduce trail braking.** The controller supports a `--trail-brake` flag that scales brake demand down proportional to steering demand. We disabled it for the submission because it needed more per-segment tuning than we had time for.

3. **Formalize the RL layer.** Not for Corkscrew — a rule-based controller is the right shape for a single-lap, single-track problem — but for a hypothetical multi-track future season, we'd take the segment YAML as an action space and treat the per-segment parameters as targets for a Bayesian optimizer.

---

## Thanks

Thanks to IBM for building the Racing League and to our professors at Miami Dade College. Everything you see here is reproducible from the public repo — take it apart, break it, make it faster.

**FINN-ISH LINE** — Louis Rodriguez, Daniel Pino, Javier Perez-Hickman.

*Follow the code: [github.com/LouisRodriguez12101815/ibm-racing-league-submission](https://github.com/LouisRodriguez12101815/ibm-racing-league-submission).*
