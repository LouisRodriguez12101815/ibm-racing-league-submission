# Submission Packet (paste into IBM Office Form)
Single source of truth for the final submission fields. Copy each `VALUE` line directly into the corresponding field at https://ibm.biz/TORCSForm.
## Required fields
### 1) Country
- **VALUE:** United States

### 2) University name
- **VALUE:** Miami Dade College

### 3) Course name
- **VALUE:** AI Models

### 4) Team name
- **VALUE:** MDC Racing

### 5) Team contact email
- **VALUE:** louis.rodriguez006@mymdc.net

### 6) Standing start lap time (used to determine who qualifies)
- **VALUE:** 143.96s (02:23.96)
- **Evidence:** telemetry archived at `telemetry/runs/2026-06-30T22-53-33/`; manifest reports `best_lap_seconds: 143.96`, `final_damage: 0.0`, `laps_completed: 1`
- **Notes:** standing start, Corkscrew, IBM F1 car, 0 damage, no off-tracks. Reproducible with `scripts/demo_submission_win.ps1` (Windows) or `scripts/demo_submission_mac.sh` (Mac/Wine).

### 7) Fastest lap video link (accessible)
- **VALUE (share link):** https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-lap-corkscrew-2-23-96.mp4
- **Sharing:** Public read on AWS S3 (no login required, direct MP4 stream)
- **Video contents:** Full-screen TORCS capture with "Miami Dade College — MDC Racing" overlay, standing start, single lap on Corkscrew, ends on Race Results screen showing 02:23.96.

### 8) Team video link (≤3 minutes, accessible)
- **VALUE (share link):** [FILL IN after recording and uploading to S3]
- **Sharing:** Same S3 bucket (`mdc-racing-ibm-submission-637675605360`) — upload with `aws s3 cp <file> s3://mdc-racing-ibm-submission-637675605360/team-video.mp4 --content-type video/mp4`
- **Script:** see `docs/team-video-script.md`

### 9) GitHub repo link (accessible)
- **VALUE (repo URL):** https://github.com/LouisRodriguez12101815/ibm-racing-league-submission
- **Accessibility:** Public (verify with `gh repo view LouisRodriguez12101815/ibm-racing-league-submission --json visibility`)

### 10) SkillsBuild badges slides link (Google Slides, accessible)
- **VALUE (share link):** [FILL IN after creating slides + sharing]
- **Sharing:** Anyone with link can view
- **Slides content:** see `docs/skillsbuild-slides.md`

### 11) AI Race Blog link (public)
- **VALUE (URL):** [FILL IN after publishing to Medium]
- **Platform:** Medium
- **Source:** `blog/blog-final.md`
- **Blog should embed/link:**
  - Fastest lap video (S3 URL above)
  - Team video (S3 URL when ready)
  - Repo: https://github.com/LouisRodriguez12101815/ibm-racing-league-submission

### 12) Bespoke F1 car livery file link (accessible)
- **VALUE (share link):** https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc_racing_livery.jpg
- **Local file:** `assets/mdc_racing_livery.jpg`
- **Sharing:** Public read on AWS S3
- **Design:** MDC Racing livery — deep royal blue, gold accents, IBM AI branding, university identifier

### 13) SkillsBuild certificate (bonus reference)
- **URL:** https://skills.yourlearning.ibm.com/certificate/share/34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAgImxlYXJuZXJDTlVNIiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQiIDogIkFMTS1DT1VSU0VfNDA1ODkxNCIKfQ21b3a5fd18-10

---

## Last-mile link checks (before you click Submit)
1. Open each S3 URL in an incognito window — both should stream/display immediately.
2. Open the Slides link in an incognito window — should show "Viewer" access.
3. Open the Medium blog link in an incognito window — should render publicly.
4. Open the repo URL in an incognito window — README should render.
5. Verify lap-video overlay is legible and Race Results screen is visible at the end.
