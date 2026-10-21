---
layout: default
title: Evidence and blockers
permalink: /evidence-and-blockers.html
---

# Evidence register and session blockers

Last reviewed: 2026-10-21 (UTC). This is a source/inspection record, not an automated refresh feed. Values below are tagged with their provenance. Organizer-confirmed is reserved for a submission-page receipt; none was available in this session.

## Official sources checked

| Source | What the source directly establishes | Limits / review state |
| --- | --- | --- |
| [DrivenData problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) | The task predicts fault structures; public labels are known to be incomplete; the initial test labels are expert-identified faults absent from the current public USGS database. It describes the supplied feature families and the 300 m triangular distance-weighted Tversky metric (alpha=0.2, beta=0.8). Submission format: same projected CRS/grid as training, EPSG:32611, 100 m, same bounds; one float32 band with values in [0,1], null/NaN outside. | Fetched directly during this session. Raster shape/transform must still be read from actual official sample/training files; do not infer them from another site's page. |
| [DrivenData data download page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) | Attempted retrieval resolves to DrivenData's login page. | Verified login gate. No authentication was attempted and no credentials requested. It is a blocker to downloading competition data from this environment. |
| [DrivenData public leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) | Current public page shows a top entry of **0.4413** and other current entries; this is a public leaderboard reading, not a submission receipt for our work. | Fetched during this session. It contradicts the brief's stated current high of 0.3195, so use the live leaderboard rather than stale/user-provided snapshots. No score from this repo exists. |
| [Official GEMS rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf) | Title and September 2026 edition identify it as official prize rules. | PDF text was retrievable; full rules sections still require careful review before data sharing, eligibility, or external-source use. |
| [USGS GeoDAWN data release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and) | USGS describes airborne magnetic and radiometric surveys, geophysical/geologic mapping purpose, the distinction in survey blocks/specifications, available deliverables including grids, and CC0 rights. | Official page fetched. It supports the availability of a source, not that a raster was downloaded or that an anomaly is a fault. Exact needed product/coverage not checked. DOI: [10.5066/P93LGLVQ](https://doi.org/10.5066/P93LGLVQ). |
| [GBCGE INGENIOUS project](https://gbcge.org/current-projects/ingenious/) | Project goal and official project context; page lists GDR/USGS publications including Great Basin heat flow, regional geophysical maps, conductance maps and slip/dilation tendency products. | Official institutional project page fetched. Individual data products are not included in this checkout and require licensing/coverage checks. |
| [DrivenData reference solution](https://github.com/drivendataorg/gems-prize-reference-solution) | Official reference-solution repository exists and its README says users must download competition data separately. | Repository page inspected. It is not this repo's cached stack, evaluator, or writer. No reference model was trained here. |
| [GEMSDOE32 experiment page](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html) | Page text describes its own artifact/method claims and explicitly distinguishes some projected values from scores; it reports internal holdout and model-based analyses. | Non-organizer experiment site; no receipt for the named artifact. Treat its analysis/score as site-reported unless independently corroborated. We did not download or copy its TIFF. |

## Score/leaderboard discrepancy

- The user brief describes the GEMSDOE32 artifact `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` as **0.2778**. **Evidence class: site-reported in the user's supplied registry list; not organizer-confirmed from a submission receipt.** The GEMSDOE32 site page gives an explanation of a dotted/thinned emission and owner analyses, but a site's prose is not evidence that its score is organizer-confirmed.
- The user's brief also says the current competition high is **0.3195**. **Evidence class: user-provided snapshot; stale/contradicted by the live official leaderboard fetched in this session.**
- The live official leaderboard currently displays **0.4413** at rank one. **Evidence class: organizer-hosted public leaderboard read, not a receipt for our submission.**
- Accordingly, this project cannot honestly claim to beat the requested artifact or leaderboard: no candidate has been generated or evaluated. The earlier site text also has its own timestamped leaderboard context and should not be assumed current.

These explicitly marked numbers are historical/source status facts, not `HOLDOUT-DTI` or a score for this project. Any number produced by a future experiment must be labeled `HOLDOUT-DTI` with evaluator version, withheld-positive count and 95% CI, or `ORGANIZER-CONFIRMED` only when copied from a submission receipt. A projection is never a score.

## Repository inspection (this checkout)

- Git tree: only `README.md` at start; no code, test suite, `data/`, GeoTIFF, stack, holdout evaluator, writer, site, or registry raster.
- Python environment at inspection: no `numpy`, `rasterio`, `scipy`, `scikit-learn`, or `pytest` available. No tests or raster validation could run.
- The prior-session status claim about `scripts/download_competition_data.sh`, `scripts/prepare_data.py`, a completed train/inference pipeline, and CPU metric tests does not match this checkout. These files are absent. We have not silently recreated or copied them.
- The competition's expected full grid metadata must be obtained from authorized data; no sample raster was available to verify CRS, shape, transform or bounds here.
- The list of sibling GEMSDOE experiment websites in the brief is user-provided. Only GEMSDOE32 was fetched in this session; exhaustive site-method review and raster-level duplicate tests remain undone.

## Irregularities flagged

1. **No lane specified:** the protocol references a single method paragraph “below” but the prompt does not identify that paragraph. The research shortlist is not a claim that the lane was resolved.
2. **Conflicting leaderboard snapshots:** 0.3195 in the brief is not the live official display, which currently shows 0.4413. Do not plan against stale leaderboard values.
3. **Data/template absent:** the promised project scripts and shared evaluator/writer are not in this branch. Reuse requirement cannot currently be satisfied.
4. **No validation or uniqueness evidence:** registry rasters absent; both continuous-surface and final-dot checks are impossible. No unique TIFF can be substantiated.
5. **No safe download:** no generated TIFF or format receipt exists. Do not submit a file from this repo.

## Next-session checklist

- [ ] Restore shared template from its authoritative location; identify exact versions and owners for cached stack, evaluator, writer and raster registry.
- [ ] Obtain authorized competition data locally, verify archive checksums and license/competition rules; keep gated data out of Git.
- [ ] Verify grid metadata against the official sample file and data description.
- [ ] Confirm the assigned method lane, then run the first preregistered candidate and all single-feature canaries on spatial whole-segment buffered folds.
- [ ] Emit evidence card with `HOLDOUT-DTI`, evaluator version, withheld positives, 95% CI, surface/dot registry tests and hashes. Record negative results.
- [ ] Only on a passed holdout and duplicate gate, produce a project-authored TIF using the shared writer and re-read/validate the final bytes. Publish a download CTA only when it is clearly marked ready/not-ready.
- [ ] The static source-linked site and GitHub Pages workflow have been added, but publishing has not been observed; enable/verify Pages with GitHub Actions after merge. The site does not auto-refresh the leaderboard. Build a source-verified feed with staleness/error indicators before describing it as current.
- [ ] Perform a sourced literature review of structural controls and geothermal indicators in the GeoDAWN / Great Basin setting. The shortlist is a set of candidate mechanisms, not a completed literature survey.
