# Submission guide — IBM AI Racing League (TORCS)

This document maps every field in the IBM submission form to a concrete artifact and provides a reproducible run/record workflow for the **standing-start Corkscrew** lap.

If you want Claude Code to finish the remaining submission artifacts (scripts, slides text, blog final, checklists), use:
- `docs/claude-code-submission-playbook.md`

## Form fields → what you submit

1. Country
Fill manually.

2. University name
Fill manually.

3. Course name
Fill manually.

4. Team name
Fill manually. Use the exact team name that appears on your fastest-lap video overlay.

5. Team contact email
Fill manually.

6. Standing start lap time
Use the **Race Results** screen time for your best clean standing-start lap.

Recommended: run with logging enabled (default) so the run is archived under `telemetry/runs/`.

7. Link to video of your standing start fastest lap (Google Drive link)
Upload the fastest-lap video to Google Drive and set sharing so IBM can access it.

Minimum checks:
- Drive sharing: **Anyone with the link can view**
- Video shows **full-screen TORCS** (per the form note)
- Video includes an overlay showing **University name + Team name**

8. Link to your team video (≤ 3 minutes)
Upload the team video to Google Drive and set sharing so IBM can access it.

Content checklist (from form text): team, course, uni, dev strategy, **how you used IBM Granite**, and **IBM SkillsBuild badges**.

Recommended outline: `docs/team-video-outline.md`.

9. GitHub repo link (accessible)
This repo is currently private. Before you submit, ensure it is accessible to IBM judges.

Options:
- Make the repo public temporarily (fastest). Example:
  - `gh repo edit LouisRodriguez12101815/ibmRacingLeague --visibility public`
- Keep it private and add the specific IBM/judge GitHub accounts as collaborators.

10. Presentation slides showing completed IBM SkillsBuild badges
Create a Google Slides deck that includes:
- Badge screenshots (images)
- Badge verification links

Recommended outline: `docs/skillsbuild-badges-slides-outline.md`.

11. Link to your AI Race Blog
Publish a blog post that tells your team’s story and embeds/links:
- Fastest lap video
- Team video
- Repo link

Draft exists at `blog/phase4-blog-draft.md` — update it and publish (Medium/WordPress/etc.).

12. Bespoke F1 car livery file (Google Drive)
Create a custom livery that includes your **university logo** and **team identifier**, then upload the livery file to Google Drive and share it (anyone-with-link view).

If you need a lightweight editor, the project resources suggest GIMP.

---

## Current baseline run (for recording the submission lap)

We keep the currently promoted “locked baseline” documented in `docs/current-submission-baseline.md`.

Driver command (works for Mac+Wine or Windows as long as `scr_server` is running and `snakeoil3_gym.py` is available):

- Segment config: `telemetry/segments_baseline_current.yaml`
- Controller flags: `--full-pedal-brake --lookahead 150 --lookahead-decel 9.0`

---

## Mac + Wine: end-to-end run + post-lap analysis

### Prereqs
- Wine installed
- IBM TORCS Quick Start bundle extracted (see `docs/mac-setup-guide.md`)
- `GYM_TORCS_DIR` set to the folder containing `snakeoil3_gym.py` (from the TORCS bundle)

Example (if you extracted to `~/torcs/gym_torcs`):
- `export GYM_TORCS_DIR="$HOME/torcs/gym_torcs"`

### Step 1 — Launch TORCS (Terminal 1)
From the TORCS install folder:
- `wine wtorcs.exe`

Then in the TORCS UI:
- Race → Quick Race → Configure Race
- Track: `road/corkscrew`
- Drivers: `scr_server 1` only
- Laps: `1`
- Accept → New Race

Expected: TORCS looks frozen / “Not Responding” while it waits for the Python driver. That is the normal SCR workflow.

### Step 2 — Run the Python driver (Terminal 2)
From the repo subdirectory `ibmRacingLeague/`:
- `./scripts/demo_submission_mac.sh`

Or run directly:
- `python3 src/driver_baseline.py --segments telemetry/segments_baseline_current.yaml --full-pedal-brake --lookahead 150 --lookahead-decel 9.0 --notes "submission run"`

### Step 3 — Validate and generate post-lap reports
After the lap completes:
- `./scripts/post_lap.sh --segments telemetry/segments_baseline_current.yaml`

Outputs are written into the latest `telemetry/runs/<timestamp>/` folder (e.g. `post_lap.md`, `segment_report.md`).

---

## Video production tips (fastest lap video)

- Record at a resolution that produces a true full-screen capture (avoid windowed “letterboxed” recordings).
- Include the overlay text for the whole video: **<University> — <Team Name>**.
- After the lap, briefly show the Race Results screen so the lap time is unambiguous.

If you want to automate overlays later, `ffmpeg` can burn text onto the video (optional).