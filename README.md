# IBM AI Racing League — Submission Package

**Team:** FINN-ISH LINE
**University:** Miami Dade College
**Course:** AI Models
**Deadline:** 2026-07-01
**Best clean lap:** 143.96s (02:23.96) — submission run 2026-06-30T22-53-33, 0 damages

## Submission Fields

| Field | Value / Status |
|---|---|
| Country | United States |
| University | Miami Dade College |
| Course | AI Models |
| Team name | FINN-ISH LINE |
| Team contact | louis.rodriguez006@mymdc.net |
| Lap time | **143.96s (02:23.96)** — standing start, Corkscrew, IBM F1 |
| Fastest lap video | ✅ https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-lap-corkscrew-2-23-96.mp4 |
| Team video (≤3 min) | ⏳ Record from `docs/team-video-script.md` |
| GitHub repo | https://github.com/LouisRodriguez12101815/ibm-racing-league-submission |
| SkillsBuild slides | ⏳ Create in Google Slides from `docs/skillsbuild-slides.md` |
| AI Race Blog | ✅ https://medium.com/@louis.rodriguez006/ibm-bobs-reward-shaper-keep-us-moving-2569b0835838 |
| LinkedIn post | ✅ https://www.linkedin.com/posts/cloud-louis_ibmskillsbuild-ibmairacingleague-python-activity-7454140320872849408-LGgZ |
| Livery file | ✅ https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc_racing_livery.jpg |
| SkillsBuild certificate | https://skills.yourlearning.ibm.com/certificate/share/34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAgImxlYXJuZXJDTlVNIiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQiIDogIkFMTS1DT1VSU0VfNDA1ODkxNCIKfQ21b3a5fd18-10 |

## Team

All members contributed as team members to design, telemetry, testing, and documentation.

- **Louis Rodriguez** — Team lead
- **Daniel Pino**
- **Javier Perez-Hickman**

## Repo Map

```
├── README.md                              ← You are here
├── submission-verification-report.txt      ← Full verification checklist
├── poll-data.json                          ← Team name poll results (Borda count)
│
├── src/
│   └── driver_baseline.py                 ← AI driver (snakeoil3 subclass)
│
├── scripts/
│   ├── demo_submission_win.ps1            ← Run the baseline lap on Windows (PowerShell)
│   ├── demo_submission_mac.sh             ← Run the baseline lap on macOS/Wine
│   ├── post_lap.sh                        ← Post-lap telemetry analysis (Mac/Linux)
│   ├── post_lap_verify.py                 ← Cross-platform clean/damage verifier
│   ├── log_telemetry.py                   ← Telemetry logger used by the driver
│   ├── overlay.html                       ← Branded overlay for screen recording
│   └── s3-public-read-policy.json         ← S3 bucket policy for submission assets
│
├── telemetry/
│   ├── segments_baseline_current.yaml     ← Locked baseline segment map (Corkscrew)
│   └── runs/                              ← Per-run archives (frames.ndjson + manifest.json)
│
├── docs/
│   ├── submission-packet.md               ← Form fields with evidence
│   ├── final-checklist.md                 ← Last-mile verification checklist
│   ├── current-submission-baseline.md     ← Run 071 baseline documentation
│   ├── team-video-outline.md              ← Team video script outline (≤3 min)
│   ├── team-video-script.md               ← Team video script (fill in details)
│   ├── skillsbuild-badges-slides-outline.md ← SkillsBuild slides outline
│   ├── track-map.md                       ← Corkscrew track segment map
│   ├── track-map.png / track-map-v*.png   ← Track maps (v8–v11)
│   └── submission.md                      ← Original submission notes
│
├── blog/
│   ├── phase4-blog-draft.md               ← Original comprehensive blog draft
│   └── blog-final.md                      ← ✅ Medium-ready polished blog post
│
├── assets/
│   └── mdc_racing_livery.jpg              ← FINN-ISH LINE F1 livery (royal blue/gold)
│
└── S3-CLEANUP-EMAIL.md                    ← Self-reminder to delete AWS S3 bucket post-judging
```

## Reproducing the submission lap

**Windows** (from repo root):

```powershell
.\scripts\demo_submission_win.ps1
```

**Mac/Wine** (from repo root):

```bash
./scripts/demo_submission_mac.sh
```

Both invoke the same `src/driver_baseline.py` with the same `telemetry/segments_baseline_current.yaml`, producing a clean lap around 143.96s. TORCS must already be at `road/corkscrew` with `scr_server 1` as the only driver and 1 lap configured. Verify with `python scripts/post_lap_verify.py`.

## Remaining Tasks (in order)

1. ✅ **Fastest lap video recorded and uploaded** to S3 (see submission-packet.md, field 7)
2. ✅ **Livery uploaded** to S3 (see submission-packet.md, field 12)
3. ⏳ **Record team video** (≤3 min) using `docs/team-video-script.md`
4. ⏳ **Create SkillsBuild Google Slides** using `docs/skillsbuild-slides.md`
5. ✅ **Blog published on Medium:** "IBM Bob's Reward Shaper: Keep Us Moving"
6. ⏳ **Upload team video** to the same S3 bucket (`aws s3 cp ... s3://mdc-racing-ibm-submission-637675605360/mdc-racing-team-video.mp4 --content-type video/mp4`)
7. ⏳ **Paste all values** from `docs/submission-packet.md` into the form: https://ibm.biz/TORCSForm
8. ⏳ **Post-submission cleanup:** delete the S3 bucket per `S3-CLEANUP-EMAIL.md`
