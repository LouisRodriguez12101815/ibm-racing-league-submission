# Team video script — MDC Racing (≤ 3 minutes)
Read this straight through. Total runtime target: **2:45–3:00**.
Speaker: Louis Rodriguez (team lead). Other members appear on-camera at the intro if available.
Recording guidance at the bottom.
---

## [0:00–0:12] Title card + intro

**On-screen:** Title card
`Miami Dade College — AI Models`
`Team MDC Racing — IBM AI Racing League 2026`

**Voice-over:**
> "Hi, we're MDC Racing from Miami Dade College. We're competing in the IBM AI Racing League 2026 for our AI Models course."

---

## [0:12–0:35] Who we are

**On-screen:** Team photo or names list

**Voice-over:**
> "Our team is Louis Rodriguez, Daniel Pino, and Javier Perez-Hickman. We built an autonomous AI driver for TORCS that runs a standing-start lap on the Corkscrew track using the IBM F1 car."

---

## [0:35–1:05] What we built

**On-screen:** Show `src/driver_baseline.py` in an editor, then `telemetry/segments_baseline_current.yaml`.

**Voice-over:**
> "Our driver is a Python controller that connects to TORCS through the SCR `scr_server` UDP protocol. It reads a YAML segment map that defines per-corner target speeds and racing-line targets around the whole lap. The controller is rule-based — no neural network in the control loop — so every decision is traceable back to a physics-grounded parameter."

---

## [1:05–1:40] Strategy — how we got faster

**On-screen:** Show a track map (`docs/track-map.png`) and briefly a per-run comparison.

**Voice-over:**
> "We started at over three minutes per lap. We drove the time down to two minutes and twenty-three point ninety-six seconds — a clean lap, zero damage — through three techniques. First, we log every run to a structured telemetry archive so we can compare configs objectively. Second, we tune per-segment target speeds and racing-line entry, apex, and exit positions. And third, we use a physics-based lookahead brake controller that pre-computes brake points from assumed deceleration."

---

## [1:40–2:15] How we used IBM Granite

**On-screen:** Show VS Code with the Continue extension open, Granite selected as the model.

**Voice-over:**
> "IBM Granite is our offline strategy analyst. We run Granite locally through Ollama and use the Continue extension in VS Code. After each run, we paste the per-segment report into Granite and ask where we're losing time. In one concrete example, Granite identified that we were exceeding our hairpin entry-speed targets but losing time on exit line quality. It generated a new segments YAML with wider exit positions that projected two to three seconds of re-acceleration gain. Granite doesn't touch the steering wheel — it makes our per-run decisions faster and better reasoned."

---

## [2:15–2:40] IBM SkillsBuild

**On-screen:** SkillsBuild badge screenshot with verification URL visible.

**Voice-over:**
> "Every team member completed IBM SkillsBuild coursework in AI models and generative AI foundations. The badge library gave us shared vocabulary for the tradeoffs between rule-based control, supervised learning, and reinforcement learning, and helped us commit early to a deterministic controller instead of chasing an RL solution that wouldn't have converged in the timebox."

---

## [2:40–3:00] Wrap + where to find our work

**On-screen:** Show the GitHub repo URL and blog URL on the title card.

**Voice-over:**
> "Our fastest lap video, code, telemetry, and blog are all in our GitHub repo: `github.com/LouisRodriguez12101815/ibm-racing-league-submission`. Thanks to IBM and to our professors at Miami Dade College. We're MDC Racing — see you on the leaderboard."

---

## Recording guidance
- **Setting:** Quiet room, single light source in front of speaker, laptop or phone at eye level.
- **Audio:** Use a headset or lav mic if possible. Room mic is fine if the room is quiet.
- **Screen recording:** Use OBS to capture the code/config/track-map cutaways. Record VO live over the screen recording, or record VO separately and drop the cutaway B-roll on a second track in a simple editor (Clipchamp, preinstalled on Windows, is enough).
- **Length target:** 2:45–3:00. If you overshoot 3:00 the form will reject the file.
- **Export:** MP4 H.264, 1080p or 720p.
- **Upload:** Same S3 bucket as the lap video. Example command:

```powershell path=null start=null
aws s3 cp "C:\Users\AlexI\Videos\mdc-racing-team-video.mp4" `
  s3://mdc-racing-ibm-submission-637675605360/mdc-racing-team-video.mp4 `
  --content-type video/mp4
```

The resulting public URL will be `https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-team-video.mp4` — paste that into field 8 of the submission packet.
