# Standing project prompt — re-read at the start of every session

This file records the operative requirements supplied by the project owner. The README is the short operational checklist; this file carries the full gates for research and release. Historical scores supplied by the owner are context only unless their exact artifact and official receipt are available.

## Objective

Build a useful, scientifically grounded, auditable project for DOE's Geologic Enhanced Mapping System (GEMS) Prize Challenge (DrivenData #306). Predict faults that are not present in the public USGS/INGENIOUS fault catalogue using data that can be shared with the sponsor under applicable licences. The main deliverable, when evidence permits, is an easy-to-find single-band GeoTIFF with a unique name and short note. The site must make it unmistakable whether any file is safe to download and whether it is approved to submit.

## Parallel-run protocol (binding)

1. **Lane.** Work only on the single method paragraph assigned to this session. Before placement and on final dots, compare candidate surfaces/rasters against every registry raster. A rank-correlation above 0.90 or more than 70% of dots within 3 pixels of one registry raster is a duplicate: log it and stop. Do not substitute another lane when the assigned paragraph is missing.
2. **Reuse, don't rebuild.** Use the shared template's cached feature stack, `evaluate_holdout.py`, and `submission_writer.py`. Hide and recover whole fault segments with a buffer. Derive every catalogue-based feature only from visible faults. Mask visible faults pixel-exactly. Score pooled distance-weighted Tversky (α=0.2, β=0.8; 300 m triangular kernel). Fix a shared-tool defect once in the shared template and report it; do not maintain a private fork.
3. **Evidence labels.** A reported project score must be either HOLDOUT-DTI, with evaluator version, number of withheld positives, and a 95% confidence interval, or ORGANIZER-CONFIRMED copied from the submission-page receipt for the exact artifact. A projection is never a score. A public leaderboard row is not a receipt for this project's file.
4. **Leakage canary.** Evaluate every feature alone on the holdout first. AUC > 0.90 is treated as leakage until proven otherwise.
5. **Run card.** Finish an experiment with one JSON card containing: hypothesis; mechanism; named non-fault process that could mimic it; HOLDOUT-DTI and CI; registry correlation/overlap; raster SHA-256; validator output (no NaN inside footprint, values in [0,1], CRS/shape/transform match); submission name and note of at most 140 characters; verdict `promote` or `negative`. Negative results are deliverables.
6. **Budget and selector.** Stop after three experiments or two hours, whichever comes first. Do not pick a competition submission. Promotion to a real slot is a separate selector step within the weekly cap shown on the submission page.

## Research requirements

Before implementation, write down 3–5 hypotheses not already tried, with the specific data layer(s), physical signature, why it could reveal a fault absent from the catalogue, how it differs from prior methods, likely non-fault mimics, expected improvement relative to implementation cost, and evidence for data availability/licensing. Rank candidates qualitatively if there are no measurements; never present a forecast as a score. A candidate requiring new external data is not viable until the exact official source and practical availability are checked.

The top candidate must beat the frozen spatially blocked holdout best before any submission slot is considered. Research and testing must be reproducible and use official, verifiable sources. Record unresolved source, data, and provenance questions as irregularities rather than filling gaps with assumptions.

## Submission format and user experience

The official problem page requires one GeoTIFF for all faults in the region: same projected CRS as training data (UTM zone 11N, EPSG:32611), 100 m resolution, same bounds, outside-bound cells null/NaN, one 32-bit float layer, predicted values in [0,1]. A single-band GeoTIFF or a ZIP containing one GeoTIFF is accepted per the submission form. The project home page must show at a glance:

- exact candidate filename and easy download control only when available;
- `OK TO DOWNLOAD` and `OK TO SUBMIT` as separate explicit decisions;
- current validation, uniqueness, holdout, and score evidence;
- a unique submission name and a short note (≤140 characters);
- a separate executive-summary page explaining the competition upload process.

Do not call a file approved solely because it passes format checks. Do not use a weekly slot unless a separate selector authorizes it.

## Mission and core values

- **Maximize P(Win):** weigh tradeoffs, assess risk, and use scarce time and submission capacity on evidence that improves the probability of success.
- **Own the Outcome:** own results end to end; diagnose and disclose failures; treat negative results as signals and improve the system without overclaiming.

## Official references to consult

- [Competition home](https://www.drivendata.org/competitions/306/competition-doe-gems/)
- [Problem description, data, metric, and submission format](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/)
- [Competition about page](https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/)
- [Data download page (login required)](https://www.drivendata.org/competitions/306/competition-doe-gems/data/)
- [Official leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/)
- [Official rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf)
- [DrivenData reference solution](https://github.com/drivendataorg/gems-prize-reference-solution)
- [USGS GeoDAWN release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and)
- [DOE GDR / INGENIOUS dataset](https://gdr.openei.org/submissions/1391)
- [INGENIOUS project](https://gbcge.org/current-projects/ingenious/)

## Current session addendum — 2026-10-21

The supplied brief did not identify a single method paragraph for this run. At session start the checkout contained only `README.md`; this review added site and documentation files, but there is still no template pin, feature cache, evaluator, writer, registry, competition data, or sample grid. Therefore the lane and all required preflight/holdout/validation gates are unavailable. **No experiment was run, no TIFF was created, no submission slot was selected.** The correct release state is `OK TO DOWNLOAD: NO FILE` / `OK TO SUBMIT: NO`. See `docs/irregularities.md` and `evidence/run_card.json`.

The historical H33 score and leaderboard values in the user's brief are not treated as receipts. The current official public page and the original GEMSDOE32 page are linked and discussed in `docs/research/why-h33-0.2778.md`.
