# Team video script (≤ 3 minutes)

NOTE: This file is intended to be finalized by Claude Code.

## Inputs needed
- University name:
- Course name:
- Team name:
- Team members + roles:
- SkillsBuild badges completed (names + links):
- Final standing-start lap time + run ID (optional):

---

## Script (draft)

[0:00–0:10] Title card
“<University> — <Course>”
“Team <Team Name> — IBM AI Racing League (TORCS)”

[0:10–0:35] Who we are
Hi, we’re <names>, from <University>, studying <Course>. In this project we built an autonomous driver for TORCS to complete a standing-start lap on the Corkscrew track.

[0:35–1:10] What we built
Our driver is a Python controller that connects to TORCS using the SCR scr_server interface and drives using real-time sensor input. We use a segment map YAML file to set target speeds and racing line targets around the track.

[1:10–1:55] Strategy (how we got faster)
We improved lap time by:
- Logging every run to a structured telemetry archive
- Iterating on per-segment target speeds and racing line
- Using physics-based lookahead braking

[1:55–2:35] How we used IBM Granite + SkillsBuild
IBM Granite helped us offline: reviewing controller code, summarizing telemetry, and proposing safer/faster adjustments. We also completed IBM SkillsBuild badges, which directly helped us structure our workflow and communicate our approach.

[2:35–3:00] Wrap + where to find our work
Our submission includes our fastest-lap video, our repo, our blog, and our SkillsBuild badge slides. Thanks for watching.
