# Team video — read-along script + visuals
Target runtime: **2:45–3:00**.
Speaker: Louis Rodriguez (team lead).
Visuals: ten branded PNGs under `docs/video-visuals/`. Bring each up full-screen at the timestamp indicated. Total: 10 cards.
Recording tools: **OBS** to capture face-cam + screen; **Clipchamp** (preinstalled on Windows) to arrange cutaways and export MP4 H.264 1080p.
---

## How to record this

1. Put the ten PNGs in an image viewer / slideshow (e.g. Windows Photos → set to full-screen). Advance manually as you speak.
2. In OBS: create a scene with (a) your webcam picture-in-picture in a corner, (b) a Display Capture of the monitor showing the PNGs. Record.
3. Read each block below verbatim. Slow, clear, natural pace.
4. Export from OBS or Clipchamp as `mdc-racing-team-video.mp4`.
5. Upload to S3 (command at the bottom).

**Read the words in the "SAY" blocks. Change the PNG at the timestamp before each block.**

---

## [0:00–0:12] — SHOW `01-title.png`
**SAY:**
> "Hi, we're MDC Racing from Miami Dade College. This is our submission for the IBM AI Racing League 2026, from our AI Models course."

---

## [0:12–0:32] — SHOW `02-team.png`
**SAY:**
> "Our team is Louis Rodriguez, Daniel Pino, and Javier Perez-Hickman. Three teammates, one goal: get an autonomous driver around the Corkscrew track in the IBM F1 car, standing start, single flying lap."

---

## [0:32–1:00] — SHOW `03-what-we-built.png`
**SAY:**
> "What we built is a rule-based Python controller. It connects to TORCS over the SCR `scr_server` UDP protocol and reads a YAML segment map that defines per-corner target speeds and racing lines. No neural network in the control loop — every decision traceable back to a physics parameter we can inspect."

---

## [1:00–1:22] — SHOW `04-lap-time.png`
**SAY:**
> "Here's our submission lap: two minutes, twenty-three point ninety-six seconds. Clean. Zero damage. Standing start. We started this project at three minutes and thirty-two seconds — that's a sixty-nine second improvement over the course of the season."

---

## [1:22–1:50] — SHOW `05-strategy.png`
**SAY:**
> "Three techniques got us there. One: a structured telemetry archive so we could compare configs objectively across dozens of runs. Two: per-segment tuning of target speeds and entry-apex-exit racing lines. Three: a physics-based lookahead brake controller that pre-computes brake points from assumed deceleration."

---

## [1:50–2:15] — SHOW `06-granite.png`
**SAY:**
> "IBM Granite is our offline strategy analyst — we run it locally through Ollama, integrated into VS Code with Continue. After every run we paste the per-segment report into Granite and ask where we're losing time. In one case Granite identified that we were over-hitting hairpin entry speeds but losing time on exit line quality, and it generated a new YAML with wider exit positions. Dense telemetry in, structured strategy out."

---

## [2:15–2:38] — SHOW `07-skillsbuild.png`
**SAY:**
> "Every MDC Racing team member completed IBM SkillsBuild coursework. What SkillsBuild gave us was shared vocabulary for the tradeoffs — sample efficiency versus generalization, deterministic control versus learned control, small local models versus cloud APIs. That framing is why we shipped a rule-based driver first instead of chasing a reinforcement learning solution that wouldn't have converged in the timebox."

---

## [2:38–2:48] — SHOW `08-repo.png`
**SAY:**
> "Everything is public on GitHub: `LouisRodriguez12101815 / ibm-racing-league-submission`. Reproducible: clone the repo, install TORCS, run one script."

---

## [2:48–2:56] — SHOW `09-blog.png`
**SAY:**
> "The full architecture, the Granite workflow, and the lessons learned are written up on Medium — search 'IBM Bob's Reward Shaper: Keep Us Moving'."

---

## [2:56–3:00] — SHOW `10-close.png`
**SAY:**
> "We're MDC Racing. See you on the leaderboard."

---

## After you record
Upload to the same S3 bucket as the lap video:

```powershell path=null start=null
aws s3 cp "C:\Users\AlexI\Videos\mdc-racing-team-video.mp4" `
  s3://mdc-racing-ibm-submission-637675605360/mdc-racing-team-video.mp4 `
  --content-type video/mp4
```

Paste this URL into field 8 of `docs/submission-packet.md`:
`https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-team-video.mp4`

## Recording checklist
- [ ] Quiet room; single front-facing light source
- [ ] Headset or lav mic (room mic okay in a quiet room)
- [ ] OBS scene has webcam PIP + Display Capture of the visuals
- [ ] Practice-read each block once; then record
- [ ] Total duration ≤ 3:00 (form rejects overshoots)
- [ ] Export MP4 H.264, 1080p or 720p
- [ ] Play back full duration before uploading

## Visual file map
- `docs/video-visuals/01-title.png`
- `docs/video-visuals/02-team.png`
- `docs/video-visuals/03-what-we-built.png`
- `docs/video-visuals/04-lap-time.png`
- `docs/video-visuals/05-strategy.png`
- `docs/video-visuals/06-granite.png`
- `docs/video-visuals/07-skillsbuild.png`
- `docs/video-visuals/08-repo.png`
- `docs/video-visuals/09-blog.png`
- `docs/video-visuals/10-close.png`
