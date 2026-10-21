# GEMSDOE81 — auditable GEMS fault-discovery workbench

> **Submission status: NOT READY — no competition GeoTIFF has been generated or validated.**
> The repository currently contains no data, cached feature stack, holdout evaluator, submission writer, or registry rasters. Do not download an older team's raster and submit it as this project's work. The competition data endpoint redirects to DrivenData login; no credentials or files are available in this checkout. A future artifact must pass the local spatial holdout and format/uniqueness gates before anyone considers using a competition slot.

## Start here on every session

Read this README, then [`docs/hypotheses.md`](docs/hypotheses.md) and [`docs/evidence-and-blockers.md`](docs/evidence-and-blockers.md) before proposing or implementing a method. These documents are the standing project brief, evidence register, and hand-off. Do not treat the long-term ambition of a high leaderboard rank as evidence that a model works.

## Mission and operating principles

Build an auditable, reproducible system that proposes **previously unmapped geological faults relevant to geothermal exploration** in the DOE GEMS GeoDAWN area. The competition's prediction target is fault presence, not geothermal vents themselves. Maximize the probability of a defensible result; own failures and preserve negative findings. A public leaderboard score is not proof of geological validity, and catalogue recovery is only a proxy for discovery of new faults.

The users' project brief asks us to:

- Review the competition, official rules, data, metric, and prior experiment registry; keep claims traceable to sources and distinguish measurements from hypotheses.
- Prefer the supplied feature stack and shared holdout/evaluator/writer rather than private forks. Never derive a catalogue-based feature from a fault segment hidden for validation.
- Propose a small, ranked set of scientifically motivated hypotheses before experiments. Test each feature alone as a leakage canary; an AUC above 0.90 is treated as suspected leakage until explained.
- Use spatially blocked, whole-segment hide-and-recover validation with a buffer, exact masking, pooled distance-weighted Tversky (alpha 0.2, beta 0.8, 300 m triangular kernel), and report uncertainty. Validate an idea before considering a weekly submission slot. Never spend/select a slot from this repository.
- Compare a candidate surface before placement and final dots to every available registry raster. If rank correlation exceeds 0.90 or more than 70% of dots fall within 3 pixels of a registry's dots, stop and report duplicate drift.
- Produce a single-band float32 GeoTIFF matching the official grid (CRS, shape, transform, resolution/bounds), with finite in-footprint predictions in [0, 1] and null/NaN outside. Re-open and validate the written bytes; do not infer validity from the in-memory array.
- Make a genuine project-authored raster easy to identify and download only after it passes these gates. Provide a unique name and a note of at most 140 characters. State clearly whether it is safe to submit; never imply a holdout projection is an organizer score.
- Maintain an official-source research log and an up-to-date, auditable status feed. Label reported measurements with their evidence class; preserve negative results and flag irregularities.

**Evidence labels:** `HOLDOUT-DTI` must include evaluator version, withheld-positive count, and 95% CI. `ORGANIZER-CONFIRMED` is reserved for values copied from an actual submission-page receipt. Values reported by an experiment site's own page are **site-reported**, not organizer-confirmed. Predictions/projections are never scores.

## Important findings and current blockers

- The official problem description says the task is pixelwise fault prediction. Its public problem page specifies EPSG:32611, 100 m, the training-grid bounds/shape, one float32 band, predictions in [0,1], and null/NaN outside. It defines the distance-weighted Tversky metric with a triangular 300 m kernel, alpha 0.2 and beta 0.8.
- The official data download page currently redirects to a DrivenData login. This checkout has no `data/` directory and consists only of the initial README. The prior-session claim that a data-download script, preparation script, training pipeline, and metric tests already exist is **not true of this branch**.
- There is no reusable template stack/evaluator/writer here. Creating a private imitation would violate the reuse requirement; first locate/restore the shared template and its versioned evaluator/writer, then use them.
- The user's starting page for the claimed 0.2778 result is an experiment site, not an organizer receipt. Its page explains a dotted emission/thinning strategy and presents additional owner-reported analyses. Those explain what that site claims it did, not why an organizer score was obtained. The official public leaderboard is independently readable; its current displayed leaders are different from the 0.3195 figure in the brief. See the evidence register for exact sources and caveats.
- No candidate experiment, holdout result, correlation/overlap calculation, raster hash, validator result, or competition submission has been produced by this repository. No TIF is offered for download. This is intentional rather than shipping an invalid or copied file.
- A static executive-summary site, submission guide, research pages, and GitHub Pages deployment workflow have been added under `docs/`. Publishing has not been observed; the repository's Pages setting must use GitHub Actions. The page does not yet auto-refresh the leaderboard, so it is a dated evidence snapshot—not the requested live feed.

## Research shortlist

The ranked candidate set, mechanism, confounders, known overlap with prior experiments, and evaluation gates are in [`docs/hypotheses.md`](docs/hypotheses.md). The current leading *test candidate* is a multi-scale magnetic–gravity edge-concordance surface. It is a hypothesis only; no score or superiority claim is made. Testing is blocked until the shared evaluator and competition data are present.

## Submission workflow (when a validated artifact exists)

1. Confirm data license/rules and use the official competition download or another expressly permitted source. Never commit private competition data or credentials.
2. Restore and pin the shared feature-stack, holdout evaluator, and submission writer. Record revisions and file checksums.
3. Run segment-buffered blocked holdout and per-feature leakage canaries. Save the fold-level metrics, pooled `HOLDOUT-DTI`, withheld-positive count, CI, and configuration. Compare all baselines at a stated pixel budget.
4. Perform surface and final-dot registry similarity/duplicate checks. Stop on a threshold breach.
5. Generate a fresh candidate only through the shared writer. Reopen the TIFF and verify band count, dtype, CRS, shape, affine transform, footprint mask, finite values, [0,1] range, and no invalid in-footprint cells. Record SHA-256.
6. Publish a short unique submission name and <=140-character note only after all gates pass. A user then downloads the TIFF and submits it through DrivenData; this repository does not select or spend a weekly slot.

See the official [problem description and format](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/), [competition data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/), [official rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf), and [reference solution](https://github.com/drivendataorg/gems-prize-reference-solution).

## What remains to be done

1. Restore/locate the actual shared project template, including cached features, `evaluate_holdout.py`, `submission_writer.py`, and registry raster catalog. Verify names/version/checksums rather than assume these exist.
2. Obtain the competition data through an authorized account and place it locally; check the official format/grid metadata. Do not put credentials or the gated data in Git.
3. Execute the preregistered first experiment in `docs/hypotheses.md` with one evaluator version, exact controls, all single-feature canaries, blocked folds, pooled metric and CI. Stop if leakage/duplication checks fail.
4. Only if it beats the current holdout best under the same protocol, consider generating a candidate TIFF. The current branch has not met that condition.
5. Build the requested auto-updating, source-linked site/feed and a prominent download CTA **only after** there is a verified downloadable candidate; until then the status must say “not ready”.

## Core sources

- [DrivenData: problem, metric and submission format](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/)
- [DrivenData: data page (login required)](https://www.drivendata.org/competitions/306/competition-doe-gems/data/)
- [DrivenData: current public leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/)
- [DOE/NLR: official GEMS Prize rules](https://docs.nlr.gov/docs/fy26osti/96647.pdf)
- [USGS: GeoDAWN data release](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and)
- [Great Basin Center for Geothermal Energy: INGENIOUS](https://gbcge.org/current-projects/ingenious/)
- [DrivenData: reference solution](https://github.com/drivendataorg/gems-prize-reference-solution)

See [`docs/evidence-and-blockers.md`](docs/evidence-and-blockers.md) for what was actually checked, and [`docs/hypotheses.md`](docs/hypotheses.md) for the experiment plan.
