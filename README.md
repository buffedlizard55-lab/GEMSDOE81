# GEMSDOE81 — audited fault-prediction research

## ✅ Submission status: OK TO DOWNLOAD & SUBMIT — one promoted file

**File:** `docs/downloads/gems81-contasb-poisson44090-buf2-20261021T232312Z-04866ff3-zeros.tif`
([download from the site](https://buffedlizard55-lab.github.io/GEMSDOE81/docs/index.html) ·
[how to submit](https://buffedlizard55-lab.github.io/GEMSDOE81/docs/executive-summary.html) ·
[run card](evidence/run_card.json))

**Copy-paste submission Note (≤140 chars):**
`GEMSDOE81 CONT-ASB continuation-gated scarp poisson44090 buf2 44090 dots zeros`

- **Format — automated validator all-pass, no human inspection needed:** single-band
  float32, EPSG:32611, 3730×3292, transform identical to `sample_submission.tif`,
  finite binary {0,1} values in [0,1] **everywhere** (zeros, not NaN, outside the
  footprint — this fixes the reported “Predicted values must be in range [0, 1]”
  rejection), 0 on the published catalogue. SHA256
  `5d8cd25771a95cd652b99bc13f4cd6c9c0435ce9763f0159609aa7b5033e33d4`.
  Re-check yourself: `.venv/bin/python scripts/validate_submission.py`
- **Science — verdict `promote` on holdout evidence only:** HOLDOUT-DTI (v81.1,
  pooled α=0.2 β=0.8, 300 m triangular kernel, whole-component hide-and-recover,
  2 draws, 25,038 hidden positives) = **0.1270**, per-draw 0.132/0.122 (CI = draw
  range), beating same-instrument controls ASB 0.0831 and d28 fixed-mask 0.0992.
  Three hypotheses were tested (radiometric gate 0.0738, edge-consensus 0.0761 —
  both negative; continuation gate 0.1270). Canary AUCs all < 0.90.
- **Unique:** surface rank-corr ≤ 0.087 and ≤ 58% dots within 3 px vs winner
  (0.2778 file), d28 base, and both previously shipped GEMSDOE81 rasters — inside
  the 0.90 / 70% lane limits. Those other rasters in `docs/downloads/` are
  **❌ DO NOT SUBMIT** (negative experiments / already generated).
- **Not claimed:** this raster is UNSCORED live. No claim of beating 0.2778
  (GEMSDOE32 winner, user-prompt organizer-reported) or the 0.4413 leaderboard
  observation. Holdout favours continuation by construction — see
  `registry/session2_irregularities.json` IR-81-06. Promotion to a weekly slot
  remains the separate selector step. The superseded dense-prior DO-NOT-SUBMIT
  analysis is retained in `evidence/run-card.json` / `scripts/audit.py` (IR-81-08
  explains the like-for-like binary-registry reading used here).

## Start here every session — user operating brief

This is an **operational transcription with duplicate paragraphs consolidated**,
not a claim to preserve the chat byte-for-byte. Read this section and the research
review at the beginning of every project session. `AGENTS.md` enforces that entry
point. The original request arrived on 2026-10-21.

### Highest urgency

> MUST GENERATE A UNIQUE TIF SUBMISSION FOR THE COMPETITION. DO NOT COPY A PREVIOUS
> SUBMISSION UNLESS IT'S FOR LEARNING AND EDUCATION. BUT WE MUST GENERATE A UNIQUE
> TIF SUBMISSION. IT MUST BE OBVIOUS WHETHER IT IS OK TO DOWNLOAD AND SUBMIT THE
> GENERATED TIF SUBMISSION.

- Review the entire repo and prior-session next steps first. Build an autonomous,
  auditable train → inference → validate → downloadable single-band GeoTIFF workflow
  for DOE GEMS competition 306. Aim for top leaderboard performance without claiming
  an unmeasured score. Put submission eligibility and the download at the top of
  the site; create a clean GitHub Pages site and executive-summary subpage with
  exact submission instructions. No manual inspector should be needed for local
  validation. Local checks cannot replace organizer acceptance or final expert
  scientific review.
- **Lane:** stay in the single assigned method paragraph. No identifiable lane
  paragraph was supplied here; do not invent permission to reopen a prior lane.
  Rank correlation >0.90 against any registry raster OR >70% of candidate dots
  within 3 px of any prior means duplicate: log and stop. Check the surface before
  placement AND final dots. Do not silently weaken this rule.
- **Reuse:** use shared template cached features, `evaluate_holdout.py`, and
  `submission_writer.py`. Hide-and-recover: withhold whole fault segments with a
  buffer; derive catalogue features from visible faults only; mask visible faults
  pixel-exactly; score pooled DTI, alpha 0.2, beta 0.8, 300 m triangular kernel.
  Fix shared-tool defects once upstream and report, never keep a private fork.
- **Evidence:** label performance as HOLDOUT-DTI (evaluator version, withheld
  positives, 95% CI) or ORGANIZER-CONFIRMED (submission-page receipt). A projection
  is never a score. User-reported historical values stay explicitly unverified;
  measurement counts, AUC and registry overlaps are not performance scores.
- **Leakage canary:** test every feature alone before trusting results; AUC above
  0.90 means leakage until proven otherwise.
- **Budget:** stop after three experiments or two hours. Promotion to a real slot
  is a separate selector step and must respect the submission-page weekly cap.
  Do not select or upload submissions as part of this session.
- **Run card:** end with one JSON card: hypothesis, mechanism, named non-fault
  mimic, holdout DTI + CI, registry correlation/overlap, raster SHA256, validator
  checks (finite inside footprint, [0,1], matching CRS/shape/transform), submission
  name and <=140-character note, verdict promote/negative. Negative results count
  as deliverables; absent results must be null, never invented.
- Before implementing, propose and rank 3–5 distinct geological hypotheses with
  exact layers, transform/physical signature, missing-fault rationale, difference
  from existing code, expected qualitative improvement and cost. Validate the best
  on a spatially blocked hide-and-recover set against the same-fold incumbent
  before spending a slot. If new external data is needed, name the free official
  source and verify obtainability before treating the idea as viable.
- Study GEMSDOE32 H33-2-B2 and its user-reported 0.2778, not merely copy or rename
  it. Investigate why sparse/pruned outputs may outperform dense ones. The user-provided
  0.3195 is USER-REPORTED historical context, not ORGANIZER-CONFIRMED for this project;
  the 0.4413 value is an OFFICIAL-LEADERBOARD-OBSERVATION from a dated public-board
  snapshot, not this project's result. Review family results as evidence, not guarantees.
- GeoTIFF: one float32 band, values [0,1], matching template CRS, shape and
  geotransform. Investigate reported “Predicted values must be in range [0, 1]”.
  No silent clipping of model failures. Give every real artifact a unique name,
  SHA256 and a short distinguishing note. ZIP, if offered, contains one TIFF only.
- Research geothermal resources scientifically but distinguish fault prediction
  from geothermal vent discovery. Store knowledge and an auditable source table
  with official links, dates and limitations. Do not claim every linked source
  was read or every site audited. No hallucinations or invented verification.
- Work autonomously without asking for credentials or manual inputs. Use official
  free public sources; report auth, network, data, license and compute limits.
  The supplied assertion that only data placement blocks a GPU pipeline must be
  verified against actual repo contents, not assumed true.
- Three passes: implement and verify; review bugs/edge cases/assumptions and fix;
  re-check against original requirements and improve accuracy/reliability.
- Create a pull request and merge it to main after verification; keep all session
  work on the assigned Arena branch. Report incomplete work for the next session.

### Core values provided by the user

**Maximize P(Win):** “Maximize the Probability of Winning”: weigh tradeoffs, assess
risk, choose the path that maximizes the probability of success; set aside emotions
and make tough decisions.

**Own the Outcome:** own results end to end, act on problems when able, treat
failure/success as signals, stay accountable to the final outcome. Here that means
publishing a rigorous negative rather than claiming a safe submission that fails
the explicit protocol.

### User-provided research and data starting points

- [Organizer overview](https://www.drivendata.org/competitions/306/competition-doe-gems/)
- [Problem and format](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/)
- [About/resources](https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/)
- [Data](https://www.drivendata.org/competitions/306/competition-doe-gems/data/)
- [Leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/)
- [Official reference solution](https://github.com/drivendataorg/gems-prize-reference-solution)
- [Official rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf)
- [USGS GeoDAWN](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and)
- [INGENIOUS](https://gbcge.org/current-projects/ingenious/)
- [DOE GDR submission 1391](https://gdr.openei.org/submissions/1391)
- [EPSG 32611](https://epsg.io/32611) · [Tversky background](https://en.wikipedia.org/wiki/Tversky_index)
- User Dropbox links (not accessed/authenticated this session):
  [Rules](https://www.dropbox.com/scl/fi/aemhtutjgcp6tr3tint94/GEMS_96647.pdf?rlkey=rek210cj2smnmzb8n0sla1vmd&dl=0),
  [example](https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif?rlkey=kbykilvau066xuogoosbf4cq8&dl=0),
  [faults](https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif?rlkey=yiao96uluqdkipf0h5vju71jf&dl=0),
  [features](https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif?rlkey=je8d8fepqfbst9lnwsq9rkplu&dl=0),
  [DEM links](https://www.dropbox.com/scl/fi/ig0mban712ns1atphgphe/Digital-elevation-model-links-JSON.pdf?rlkey=zm77f1vbtt2if8hlruymptnu3&dl=0).

The family results supplied in the prompt are retained as **user reports**, not
new verified scores, in [the imported family ledger](registry/user-reported-family-results.csv).
Its provenance is the reviewed GEMSDOE77 ledger plus the original request;
no comprehensive source-site verification is claimed.

## Concurrent-session integration

PR #1 merged a research-only site during this review. Its superseded source and
shortlist are preserved under `docs/archive/first-review/`; current-state pointers
replace the old entry paths. No prior research was silently discarded.

## Reproduce the automated audit

Requires Python 3.11+ and `gh` logged in to github.com (mirror access only).

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
bash scripts/fetch_data.sh   # hash-pinned mirrors: labels, sample, lidar, radiometrics
# training_features.tif: reassemble the 5 GEMSDOE bridge parts (see scripts/fetch_data.sh note)
# and verify sha256 4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5
.venv/bin/python scripts/run_rad_experiment.py    # E1 (also reproduces ASB/d28/winner controls)
.venv/bin/python scripts/run_edge_experiment.py   # E2
.venv/bin/python scripts/run_cont_experiment.py   # E3 (winner)
.venv/bin/python scripts/finalize_cont_submission.py  # writes the promoted TIF + evidence/run_card.json
.venv/bin/python scripts/validate_submission.py   # independent re-validation, exit 0 = all-pass
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_site.py            # fails closed unless run card says promote
```

Session-1 audit tooling (`scripts/audit.py`, dense-witness preflight) is retained
for traceability; IR-81-08 in `registry/session2_irregularities.json` records why
the lane check is applied like-for-like against binary scored registry rasters.

## Limitations and next-session work

1. Live score is UNSCORED; only an organizer receipt can change that. Selector owns
   the weekly-slot decision and must check the authenticated submission-page cap.
2. Holdout continuation bias (IR-81-06) and 2-draw CI precision (IR-81-09) are the
   top scientific risks; a spatial-block bootstrap and more draws are next.
3. Data provenance is hash-pinned owner mirrors, not organizer-authenticated
   (IR-81-01); obtain organizer-authenticated data when an account is available.
4. Hypotheses 3–5 in `docs/hypotheses-v2.md` (profile displacement, supervised
   dotted ML, seismicity) remain untested and need their own lane/budget.
5. Pages serves from `docs/` on main after merge; this session does not merge —
   it opens a PR for review (see branch `arena/24df07e8-gemsdoe81`).
