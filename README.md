# GEMSDOE81 — audited fault-prediction research

## Submission status: **DO NOT SUBMIT — no authorized new TIF**

[Executive summary and submission instructions](https://buffedlizard55-lab.github.io/GEMSDOE81/docs/executive-summary.html)
· [Research review](docs/research/review.md) · [Machine-readable run card](evidence/run-card.json)

**The requested unique submission was NOT generated.** The literal registry rule
rejects every nonempty in-footprint candidate: a verified registered prior is
positive throughout the footprint. Overlap would be 100%, exceeding the 70%
stop limit, regardless of geological method. We obey the stop rule rather than
copy an old submission, fabricate a success, or quietly exempt dense priors.
See [the independently recomputed proof](evidence/preflight.json).
A format-valid TIFF is not necessarily unique, scientifically promoted, accepted
by DrivenData, or a good predictor. No competition submission slot was used.

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
  it. Investigate why sparse/pruned outputs may outperform dense ones. The prompt
  gives competing leaderboard values 0.3195 and 0.4413: verify the current official
  page rather than assert both. Review family results as evidence, not guarantees.
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

## Reproduce the automated audit

Requires Python 3.11+, `gh` with access to the public GitHub blobs, and package
installation access. Full-resolution data, cached models, and restored inputs
are ignored by Git. Only small JSON reports and code are tracked.

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/restore_inputs.py
.venv/bin/python scripts/audit.py
# Expected exit 2 = verified STOP_UNIVERSAL_DUPLICATE, not a broken audit.
# Exit 3 = untrusted/missing input; exit 0 = no universal proof, NOT clearance.
.venv/bin/python scripts/audit_reference.py   # historical bytes: learning only
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_site.py
```

Shared evaluator and writer are unmodified under `vendor/gems57/`; hash-check
before use. No feature stack, model, holdout score, AUC or new candidate is claimed.
The earlier `download_competition_data.sh` / `prepare_data.py` commands do not exist
in this starting repo and are not represented as working training steps here.

## Limitations and next-session work

1. Resolve the literal dense-raster overlap contradiction in the **shared**
   protocol/registry; never silently add an exemption in this repo.
2. Obtain a unique lane assignment; audit proposed transforms across all lanes.
3. Restore the shared cached feature stack and verify organizer provenance/licensing.
4. Establish compatible buffered whole-segment holdout and incumbent, run canaries,
   then at most three experiments with pooled DTI and spatial confidence intervals.
5. Only after every gate passes, write a new TIF with the shared writer, validate
   read-back and uniqueness, expose one-click download and hand promotion to the
   separate selector. Check the authenticated submission-page cap there.

The existing Pages configuration serves main/root; the root landing page redirects
to `docs/`. The audit workflow checks the evidence and saves a Pages artifact;
legacy Pages deployment is separate and is not CI-gated by this workflow. An API
attempt to switch Pages to Actions returned HTTP 403 (integration permission).
No live data feed or leaderboard-success claim is implied. See dated [source audit](registry/sources.json).
