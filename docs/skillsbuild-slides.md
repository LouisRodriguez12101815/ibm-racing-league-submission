# SkillsBuild Badges — Google Slides content
Ready-to-paste text for each slide. Create a new Google Slides deck (16:9), use the "Simple Light" theme, and paste each slide's title + body verbatim. Add screenshots where indicated.
When done: **File → Share → General access → Anyone with the link → Viewer** → copy link → paste into field 10 of the submission packet.
---

## Slide 1 — Title
**Title:** IBM SkillsBuild Badges — MDC Racing
**Subtitle:**
Miami Dade College · AI Models
Team MDC Racing · IBM AI Racing League 2026
Louis Rodriguez · Daniel Pino · Javier Perez-Hickman

---

## Slide 2 — Summary
**Title:** What we completed
**Body:**
- Each MDC Racing team member completed IBM SkillsBuild coursework aligned to the AI Models course.
- Focus areas: AI foundations, generative AI, and applied ML tradeoffs relevant to autonomous control.
- Learning informed our decision to ship a rule-based controller instead of an RL-first architecture in the competition timebox.
- Verification links and screenshots on the following slides.

---

## Slide 3 — Badge #1 (team-shared)
**Title:** AI Foundations (or the badge that best matches your team certificate)
**Body (left column):**
- **Completed by:** Louis Rodriguez, Daniel Pino, Javier Perez-Hickman
- **Verification URL:** https://skills.yourlearning.ibm.com/certificate/share/34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAgImxlYXJuZXJDTlVNIiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQiIDogIkFMTS1DT1VSU0VfNDA1ODkxNCIKfQ21b3a5fd18-10
- **What we learned:** Vocabulary for AI system tradeoffs (deterministic vs learned control, generalization vs sample efficiency).
- **How it impacted the project:** Confirmed a rule-based baseline was the right first target before layering learning.

**Right column:** Paste badge screenshot.

---

## Slide 4 — Badge #2 (per-member, if applicable)
**Title:** [Badge name]
**Body:**
- **Completed by:** [Member name]
- **Verification URL:** [Paste share URL]
- **What we learned:** [1–2 sentences]
- **How it impacted the project:** [1 concrete example, e.g. "informed our lookahead braking model" or "helped structure our telemetry logging schema"]

Right column: badge screenshot.

*(Duplicate this slide for each additional badge/team member.)*

---

## Slide 5 — Badge #3 (per-member, if applicable)
**Title:** [Badge name]
**Body:** (same pattern as slide 4)

---

## Slide 6 — How SkillsBuild impacted the submission
**Title:** From learning to results
**Body:**
- **Deterministic controller first.** SkillsBuild coursework on the sample-efficiency vs generalization tradeoff convinced us to ship a physics-grounded rule-based driver before touching RL. That decision is why we have a clean, reproducible 143.96s lap on submission day.
- **Telemetry discipline.** SkillsBuild content on data-driven ML iteration shaped our per-run telemetry archive and per-segment reports — the same reports IBM Granite reads for offline strategy analysis.
- **Model selection framing.** We use local IBM Granite (via Ollama + Continue) for offline analysis; the SkillsBuild generative-AI content grounded our choice of a small, controllable local model over a cloud API.

---

## Slide 7 — Links
**Title:** Where our work lives
**Body:**
- GitHub repo: https://github.com/LouisRodriguez12101815/ibm-racing-league-submission
- Fastest lap video (S3): https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc-racing-lap-corkscrew-2-23-96.mp4
- Livery (S3): https://mdc-racing-ibm-submission-637675605360.s3.amazonaws.com/mdc_racing_livery.jpg
- Blog (Medium): [Paste Medium URL after publishing]

---

## Where to store badge screenshots in this repo
Drop image files into `docs/skillsbuild/` (create the folder if needed) so they're easy to drag into the Google Slides deck. Example filenames:
- `docs/skillsbuild/ai-foundations-louis.png`
- `docs/skillsbuild/generative-ai-daniel.png`
- `docs/skillsbuild/ml-foundations-javier.png`
