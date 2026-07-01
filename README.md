# IBM AI Racing League — Submission Package

**Team:** MDC Racing
**University:** Miami Dade College
**Deadline:** 2026-07-01
**Best clean lap:** 143.306s (2:23.31) — Run 071, 0 damages

## Submission Fields

| Field | Value / Status |
|---|---|
| Country | United States |
| University | Miami Dade College |
| Course | Introduction to Artificial Intelligence / COP2XXX |
| Team name | MDC Racing |
| Team contact | louisrodriguez12101815@gmail.com |
| Lap time | **143.306s (02:23.31)** — standing start, Corkscrew, IBM F1 |
| Fastest lap video | ⏳ Record then upload to Google Drive |
| Team video (≤3 min) | ⏳ Record then upload to Google Drive |
| GitHub repo | https://github.com/LouisRodriguez12101815/ibmRacingLeague |
| SkillsBuild slides | ⏳ Create in Google Slides, then share |
| AI Race Blog | ⏳ Publish, then paste link |
| Livery file | ⏳ Upload `assets/mdc_racing_livery.jpg` to Google Drive |
| SkillsBuild certificate | https://skills.yourlearning.ibm.com/certificate/share/34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAgImxlYXJuZXJDTlVNIiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQiIDogIkFMTS1DT1VSU0VfNDA1ODkxNCIKfQ21b3a5fd18-10 |

## Team

- **Louis Rodriguez** — Team lead, driver development, telemetry
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
│   ├── demo_submission_mac.sh             ← Run the baseline lap on macOS/Wine
│   └── post_lap.sh                        ← Post-lap telemetry analysis
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
│   ├── phase4-blog-draft.md               ← Excellent comprehensive blog draft
│   └── blog-final.md                      ← Blog post template (finalize from draft)
│
└── assets/
    └── mdc_racing_livery.jpg              ← MDC Racing F1 livery (royal blue/gold)
```

## Remaining Tasks (in order)

1. **Mount & install TORCS:** `open ~/Downloads/Torcs.dmg`
2. **Record fastest lap video:** `wine wtorcs.exe` + `Cmd+Shift+5` + `./scripts/demo_submission_mac.sh`
3. **Record team video** (≤3 min) using `docs/team-video-outline.md`
4. **Create SkillsBuild Google Slides** using `docs/skillsbuild-badges-slides-outline.md`
5. **Publish blog** from `blog/phase4-blog-draft.md`
6. **Upload livery** (`assets/mdc_racing_livery.jpg`) to Google Drive
7. **Paste all links into:** https://ibm.biz/TORCSForm
