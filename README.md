# GEMSDOE81

## ⭐ EXECUTIVE SUMMARY — DOWNLOAD & SUBMIT (start here)
**✅ OK TO DOWNLOAD AND SUBMIT — format-validated automatically, no human inspection needed.**
[**⬇ Download the submission TIF: `gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif`**](docs/downloads/gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif) (also on the GitHub Pages site: `docs/index.html`)
- **Submission Note (75/140 chars, copy-paste):** `GEMSDOE81 ASB scarp-pair x basement-step poisson44090 buf2 44090 dots zeros`
- Validator (in-repo, fails closed): single-band float32 · EPSG:32611 · 3730×3292 · transform = sample submission · **finite values in [0,1] everywhere (zeros, not NaN, outside footprint — fixes the "Predicted values must be in range [0, 1]" rejection)** · 0 on catalogue · sha256 `e548bc657c9141f17af11b2c9063894eb0abcb4665504f22e1d3dde3ce504402`.
- ⚠️ **Science verdict: negative** — safe to submit, but HOLDOUT-DTI did not beat the control (below); do not claim/ expect >0.2778. Full how-to: `docs/executive-summary.html`.

> Prompt of record (condensed, read every session): Generate a UNIQUE TIF submission; do not copy a previous submission; it must be obvious whether it is OK to download/submit; automated (not human) inspection must validate it. Parallel-run protocol: stay in your lane (rank-corr ≤0.90 and ≤70% dots within 3px vs any registry raster, checked on surface and final dots); reuse shared holdout/submission-writer tools; label every number HOLDOUT-DTI (evaluator version, n hidden, CI) or ORGANIZER-CONFIRMED; leakage canary AUC>0.90 per feature; end with a JSON run card; budget ≤3 experiments / ≤2h; never write a projection as a score. Core values: Maximize P(Win); Own the Outcome.

## Why/how did `h33-h33-2-b2-…-zeros` score 0.2778 (ORGANIZER-CONFIRMED, per user/GEMSDOE32)?
Its GEMSDOE32 audit states: *"0.2708 base with every dot at d(catalogue) ≤2 px deleted (37,654 dots)"*. Mechanism (pooled DTI α=0.2 β=0.8, 300 m triangular kernel): score is earned only near **undiscovered** test faults; dots hugging the published catalogue earn ~no credit there but pay false-positive mass (denominator α·(TP+FP)+β·FN), so pruning them raised the score 0.2708→0.2778. The dotted family wins generally because a single dot covers a 300 m kernel neighbourhood — density wastes budget, spacing ≈ kernel width is near-optimal. **Can we beat it? Not claimed here:** our unique label-free surface scored lower on holdout (below); beating 0.2778 credibly needs a surface that finds off-catalogue faults better than the dotted H19-5 base, which this session's 3-experiment budget did not produce. The current leaderboard highs quoted in the prompt (0.4413 / 0.3195, inconsistent — IR-81-02) were not re-verified live.

## This lane (unique)
Antithetic-scarp-pair × basement-step coincidence (ASB): `sqrt(rank(lapneg)·rank(lappos))` from USGS 3DEP 1 m LiDAR scarps × `sqrt(rank(|∇depth_to_basement|)·rank(|∇conductivity|))`, Poisson-priority thinning 2.8 px, 44,090 dots, catalogue buffer 2 px. Non-fault mimic: paired terrace riser/paleo-shoreline over a sedimentary pinch-out. Uniqueness vs registry: **rank-corr 0.031 (winner) / 0.036 (d28); 31–33% dots within 3 px** — inside lane limits. 5 ranked hypotheses (2–5 untested, budget): `registry/hypotheses_sources_irregularities.json`.

## Results (labelled)
| raster | label | value |
|---|---|---|
| ASB shipped | HOLDOUT-DTI v81.1, 25,038 hidden positives, draw-range CI [0.0768, 0.0895] | **0.0831** |
| d28 base control | HOLDOUT-DTI v81.1 same instrument | 0.0992 |
| winner h33-2-b2 | HOLDOUT-DTI v81.1 (instrument mechanically penalises flank-pruning, IR-81-03) | 0.0043 |
| winner h33-2-b2 | ORGANIZER-CONFIRMED (user/GEMSDOE32 receipt) | 0.2778 |
| ASB shipped | live | **UNSCORED** |
Canary AUCs (all <0.90, no leakage flag): A 0.572, B 0.547, S 0.589. E3: ridge-union variant 0.0728 and batch-greedy 0.0307/0.0390 — both worse, not shipped.

## Run card (JSON)
`evidence/run_card.json` — hypothesis, mechanism, mimic, HOLDOUT-DTI+CI, registry corr/overlap, raster sha256, validator output, submission name+note, **verdict: negative** (format-promote, science-negative).

## Reproduce / validate
```bash
pip install -r requirements.txt
bash scripts/fetch_data.sh            # hash-pinned GitHub mirrors, fails closed (IR-81-01)
python3 scripts/finalize_submission.py
python3 scripts/validate_submission.py
python3 -m pytest tests -q
```
Limitations/next session: (1) no DrivenData auth — data are owner-mirror bytes, hash-verified not organizer-authenticated; (2) holdout cannot rank catalogue-flank strategies — a live-anchored instrument is needed before spending slots on prune variants; (3) hypotheses 2–5 untested; (4) exact greedy emitter too slow (IR-81-04).

Sources (official): DrivenData competition https://www.drivendata.org/competitions/306/competition-doe-gems/ · reference solution https://github.com/drivendataorg/gems-prize-reference-solution · USGS GeoDAWN DOI 10.5066/P93LGLVQ https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and · GDR 1391 https://gdr.openei.org/submissions/1391 · EPSG:32611 https://epsg.io/32611 · NLR 96647 https://docs.nlr.gov/docs/fy26osti/96647.pdf
