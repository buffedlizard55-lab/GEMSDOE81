# GEMSDOE81 — evidence-gated research for the DOE GEMS Prize

> **Current state (2026-10-21): NO submission TIFF exists in this repository.**
> **OK to download? NO — there is no candidate file.** **OK to submit? NO.**
> Do not submit this repository's sample, an older GEMSDOE artifact, or an unvalidated substitute.

This repository is an auditable workspace for studying previously unmapped geologic faults in the DOE GEMS Prize region. A submission will only be offered after the assigned method is identified, the shared-template workflow and data are available, a spatially blocked hide-and-recover evaluation beats the frozen local baseline, the leakage and registry-uniqueness gates pass, and an independent GeoTIFF read-back validates the competition contract. No weekly submission slot is selected here.

## Start here every session

Read this README and then [`PROMPT.md`](PROMPT.md), [`docs/irregularities.md`](docs/irregularities.md), and the current [`evidence/run_card.json`](evidence/run_card.json) before changing the project. They preserve the standing brief, protocol, blockers, and current verdict. The project site is [`index.html`](index.html); the exact submission walkthrough is [`executive-summary.html`](executive-summary.html).

## Standing project brief

- **Goal:** build a scientifically defensible system for predicting faults missing from the public USGS/INGENIOUS catalogue, with a straightforward, clearly gated GeoTIFF download path when — and only when — a candidate is promoted.
- **Maximize P(Win):** spend effort on evidence that can change the decision; do not spend a competition slot on an unvalidated idea.
- **Own the Outcome:** report negative results and defects; do not hide an error, overstate a source, or call a projection a score.
- **Research:** develop 3–5 genuinely distinct geological hypotheses, name the layers and physical signature, explain why a hidden fault could produce that signature, identify a plausible non-fault mimic, and check any external source and its access/licence before treating it as usable.
- **Reuse, do not rebuild:** use the shared template's cached feature stack, `evaluate_holdout.py`, and `submission_writer.py`. Withhold whole fault segments plus a buffer; derive catalogue features only from visible faults; mask visible faults pixel-exactly; score pooled DTI with α=0.2, β=0.8, and the 300 m triangular kernel. Fix shared-tool defects in the template, not in a private fork.
- **Gate every candidate:** run each feature alone as a leakage canary (AUC > 0.90 is leakage until proven otherwise); check rank correlation and 3-pixel dot overlap against every registry raster before placement and again on final dots; stop on a duplicate. Report HOLDOUT-DTI with evaluator version, withheld-positive count, and 95% CI, or identify an organizer score only from a submission-page receipt. Projections are not scores.
- **Run card:** include hypothesis, mechanism, named non-fault mimic, holdout DTI and CI, registry correlation/overlap, raster SHA-256, validator output, submission name and ≤140-character note, and `promote`/`negative` verdict. Budget: at most three experiments or two hours. Promotion is a separate selector decision.
- **Submission format:** one-band float32 GeoTIFF on the competition grid (EPSG:32611, 100 m, matching CRS, bounds, shape, and geotransform), probabilities/confidence in [0,1], and null/NaN outside the study bounds, as specified by the official problem page.

## Verified status and important caveats

- At session start, the local checkout contained only this README. This review added documentation/site files and `data/README.md`, but no competition data, cached stack, shared-template pin, registry, evaluator, writer, scripts, tests, or generated TIF. Therefore no holdout, leakage test, correlation/overlap check, or TIFF validation can be run here. Details: [`docs/review.md`](docs/review.md).
- The method paragraph that should assign this parallel run's lane is absent from the supplied brief. Under the parallel-run protocol, a method cannot be chosen or implemented speculatively. This is a hard stop, not permission to change lanes.
- The user-provided H33 value **0.2778** is not accompanied here by an organizer submission-page receipt. The original [GEMSDOE32 page](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html) explicitly described its 0.2747 figure as a model projection and stated that no organizer score existed for its artifacts at that time. See [`docs/research/why-h33-0.2778.md`](docs/research/why-h33-0.2778.md).
- The supplied 0.3195 leaderboard figure is historical. The official public leaderboard page was read on 2026-10-21 and displayed xiaofanhu at 0.4413 in first place. This is a dated public-board observation, not a receipt for any file in this project and not private-test performance. Always follow the live [official leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) rather than a stale copied number.
- The competition error “Predicted values must be in range [0, 1]” does not identify its cause by itself. No rejected TIFF is present here, so this repository cannot claim a fix or diagnose that file.

## What is ready now

1. [`index.html`](index.html) presents the download/submit status before any research detail.
2. [`executive-summary.html`](executive-summary.html) explains how to submit a *promoted* file and how to diagnose format rejection without pretending a submission is ready.
3. [`docs/research/why-h33-0.2778.md`](docs/research/why-h33-0.2778.md) separates metric mechanics, artifact provenance, and unverified score attribution.
4. [`docs/research/hypotheses.md`](docs/research/hypotheses.md) records a ranked, explicitly provisional hypothesis shortlist and official source availability checks.
5. [`docs/sources.md`](docs/sources.md) links official competition, DOE, USGS, NASA/ASF, and reference-solution sources.
6. [`evidence/run_card.json`](evidence/run_card.json) records why this session is negative/blocked and why there is no submission artifact.

## Official starting points

- [Competition problem description and metric](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/)
- [Official rules (NLR/DOE PDF)](https://docs.nlr.gov/docs/fy26osti/96647.pdf)
- [Competition data page (login required)](https://www.drivendata.org/competitions/306/competition-doe-gems/data/)
- [Official public leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/)
- [DrivenData reference solution](https://github.com/drivendataorg/gems-prize-reference-solution)
- [USGS GeoDAWN data release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and)
- [DOE Geothermal Data Repository: INGENIOUS regional dataset](https://gdr.openei.org/submissions/1391)

## Local preview

The site is plain HTML/CSS with no build step. From the repository root, validate its local links and fail-closed release card with:

```bash
python3 scripts/check_site.py
```

Preview it with:

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

No competition data, public leaderboard scraping, or submission upload is performed by the site.
