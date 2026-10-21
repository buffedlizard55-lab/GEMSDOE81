# Corrective repository review — 2026-10-21

## Decision and completed next steps

**DO NOT SUBMIT.** An inherited ASB TIFF exists and is easily downloadable from
all current submission pages, but only as a **negative research artifact**.
No unique competition-ready TIFF was generated here. No new geological
experiment or weekly submission slot was used. The binding literal duplicate
stop was independently reproduced before any candidate work.

Prior-session next steps were addressed first: the shared tools were hash-checked,
audit inputs restored, and the registry contradiction rechecked. The contradiction
remains; we did not silently add a dense-prior exemption or invent a lane.
Instead, we repaired contradictions in the already merged project.

## Concrete defects found and corrected

| Observation at session start | Verified in | Correction |
|---|---|---|
| Homepage said no TIFF existed; ASB page said safe to submit | `docs/index.html`, `docs/asb-candidate.html`, actual file | Every current submission page uses the same negative decision; research-only download prominently available. |
| Existing test suite failed on the inherited TIFF | Initial pytest run: one failure, 27 passes | Replace obsolete “no TIFF anywhere” assertion with hash-checked negative-artifact policy and cross-page checks. |
| Historical values called organizer-confirmed with no receipt | Legacy ASB card, finalizer and candidate page | Retracted label; 0.2778 remains USER-REPORTED. No claim to beat it or any leaderboard value. |
| Two random-draw extrema called a 95% CI | Private runner and ASB card | Preserve as reported draw range only; accepted HOLDOUT-DTI, withheld count and CI are null. |
| Canary used full catalogue; prescribed segment buffer absent | `src/gems81/holdout.py` at starting commit; build runner | Reject legacy validation as promotion evidence. Retire private runner/evaluator; use pinned shared tooling only. |
| Two-raster partial comparison bypassed dense rejection witness | Finalizer and preflight | Recompute final-dot overlap against authenticated-by-hash witness; log duplicate and stop. No full inventory clearance claimed. |
| Writer converted any float, including invalid values, to bool | `src/gems81/submission_writer.py` at starting commit | Replace with imports of shared fail-closed writer/validator. No silent repair or boolean coercion. |
| Hardcoded holdout numbers and `/tmp` inputs could republish results | Finalizer | Retire both candidate entry points with live fail-closed audit; no surface, placement or write. |
| Fetch script printed hashes without checking expectations | `scripts/fetch_data.sh` | Replace with pinned audit-input restorer; no incomplete training restore implied. |

The authoritative record is [run-card.json](../evidence/run-card.json).
The underscore card, old run JSON and old TIFF receipt now point to that record.
Historical measurements and defects are in [legacy-asb.json](../evidence/legacy-asb.json).
Original bytes/code remain in Git at starting commit
`a53c822d3c41bd94440b375ad14c529d7d1d15cb`; they are not current approvals.

## Independently checked TIFF

- Filename: `gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif`.
- SHA256: `e548bc657c9141f17af11b2c9063894eb0abcb4665504f22e1d3dde3ce504402`.
- Single float32 band, EPSG:32611, shape 3730 × 3292, 100 m pixels and matching
  sample affine transform; 44,090 positive pixels. These are byte measurements,
  not scores.
- Pinned shared `validate.py` and `gates.format_report` confirm no NaN or infinity,
  values in [0,1] everywhere, zero catalogue and outside-footprint mass.
- **REGISTRY-MEASUREMENT:** final-dot forward overlap within 3 px is 1.0 against
  SHA256 `ab0a0a62eecf066a82713b09dd49f0f638a91fa3dd81f54cc34ae89afa3872be`.
  This alone exceeds 0.70, so correlation is not needed for rejection and is null.
- Original continuous surface was not retained. We do not pretend to recompute
  its rank correlation. The candidate-independent proof covers every nonempty
  in-footprint support before placement and final dots.
- **HOLDOUT-DTI:** not run; shared evaluator version `gems57-pooled-hide-v2`,
  value/withheld positives/95% CI null. Legacy private-evaluator numbers cannot
  fill these fields. No compliant same-fold best is established in this checkout.

## Why H33 could work — and what cannot be inferred

The [previous reference byte audit](../evidence/reference_audit.json) is rerun for
learning only. It supports sparse dots and catalogue-collar deletion, not a new
geothermal discovery or verified public score. Efficient emission can reduce
redundant mass under maximum triangular coverage; pruning catalogue-adjacent dots
may help an initial-round new-fault target but can also remove unmapped strands.
This is a mechanism hypothesis, not causal attribution from a public score.

The user-reported historical 0.2778, 0.3195, and 0.4413 are not artifact-linked
organizer receipts. A prior-session dated public leaderboard observation of
0.4413 is retained as such, not checked again here. No guarantee or numerical
projection of improvement is scientifically justified. A frozen historical TIFF
that used the full fault catalogue is not a fair hide-and-recover control; rebuild
the method on fold-visible faults instead.

## Ranked candidate hypotheses — before any future implementation

The [earlier four-hypothesis table](review.md#ranked-hypotheses--proposals-only-before-implementation)
is the retained conditional shortlist, not authorization to reopen a lane.
Relative to the inherited ASB scalar gradient product, these prioritize different
observables. None is claimed novel across every family repo or viable without a
lane and verified cache. Expected value is qualitative, never a projected score.

| Priority / expected value / cost | Exact layers and signature | Missing-fault rationale; named non-fault mimic; distinction |
|---|---|---|
| First / strongest conditional value per cost / medium | RTP magnetic field, isostatic gravity anomaly, conductivity: signed cross-correlation displacement between adjacent cross-strike profiles, repeated over windows | Buried displacement without scarp; intrusive contact or interpolation seam can mimic. Tests profile offset, not ASB coincident edge magnitude. |
| Second / moderate / medium | Conductive-base depth second derivative with RTP profile phase break | Buried flexure may remain without mapped scarp; salinity front or inversion regularization can mimic. Requires signed flexure/phase relation, not a gradient product. |
| Third / plausible, lower cost-adjusted value / high | DEM tributary heads/valley mouths: repeated consistently signed piercing-point offsets | Lateral displacement may lack continuous scarp; stream capture/avulsion mimic. Tests repeated offsets, not LiDAR laplacian scarp pairs. Coarse-cache adequacy unknown; high-resolution 3DEP source bytes and coverage NOT obtainable-verified here, so not viable as a new external-data proposal. |
| Fourth / lower pending novelty audit / medium | RTP/TMI/magnetic anomaly: left/right along-strike autocorrelation length truncation stable across scales | Fabric termination may lack a strong scarp; volcanic unit boundary or leveling seam mimic. Tests texture interruption, not ASB edge amplitude. |

No new external download was needed for the rejection review. No external-data
idea was promoted as viable. The inherited [source screen](external-source-screen.md)
contains leads only, not verified target-area data coverage or licenses.

## Official sources and access limits

| Source | What was actually checked in this corrective session | Limit |
|---|---|---|
| [Official reference README, pinned](https://github.com/drivendataorg/gems-prize-reference-solution/blob/aebe92f7c8a990f0e3443451b7a825d9afd6336b/README.md) | Retrieved via GitHub API; CPU-only setup explicitly supported, GPU faster not required; data downloaded separately | Reference training notebook not executed here. |
| [Shared template, pinned](https://github.com/buffedlizard55-lab/60GEMSDOE/tree/b99591eede63c6d45c8a896255b8cd34824fa00b/src/gems57) | Local vendored files match SHA pins; shared validation/evaluator software tests run | Owner shared tooling, not organizer certification. No private tool patch. |
| [H33 source, pinned](https://github.com/buffedlizard55-lab/GEMSDOE32/tree/f62038b54dcb7767d4d997f80b033cdc3d42bef9) | Hash-verified reference raster read for learning only | No organizer receipt. |
| [Official problem](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) / [data](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) / [leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) | Prior-session source observations retained with attribution, not freshly fetched | Hosts outside sandbox outbound allowlist; no DrivenData authenticated session or weekly-cap access. |
| [Rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf), [USGS GeoDAWN](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and), [GDR 1391](https://gdr.openei.org/submissions/1391) | Official links retained for manual review | Not retrieved in corrective session; no new claims of rule, payload, license or coverage verification. |

The audit uses SHA-pinned owner mirrors, not organizer-authenticated training
inputs. Internet access is limited to GitHub and package registries. A full live
source feed, new external-data acquisition and portal acceptance are not available
here. The failed submission file was not supplied; the range-error cause remains
unknown. A geothermal fault indicator is not proof of an active vent or resource.

## Three review passes and reproduction

**Pass 1 — inspect and reconcile:** reproduce binding preflight and failing
baseline tests; independently inspect existing raster with shared tools; unify
negative state and preserve a research-only download; retract unsupported claims.

**Pass 2 — defects and edge cases:** test invalid float writer input, runner
stops, missing/corrupt inputs, changed artifact hashes, stale approval cards,
nonzero CLI failure status, all public entry paths and superseded receipts.
Do not alter pinned upstream tools; this review found defects in local wrappers
and callers, not a new shared-tool defect requiring a fork.

**Pass 3 — original requirements:** rerun all checks, rebuild site twice for
idempotency, smoke-test HTTP/download bytes and local links; verify explicit
negative card, no slot, no projection-as-score, and clean Git diff. Results are
recorded in `evidence/verification.json` in the repository.

```sh
.venv/bin/python scripts/restore_inputs.py
.venv/bin/python scripts/audit.py             # expected exit 2: binding duplicate
.venv/bin/python scripts/audit_reference.py   # historical bytes, learning only
.venv/bin/python scripts/audit_existing.py    # existing artifact checks, no experiment
.venv/bin/python scripts/validate_submission.py # exit 0 = local format, NOT approval
.venv/bin/python scripts/build_site.py
.venv/bin/python -m pytest -q
```

### Next-session priorities

1. Resolve the shared protocol's definition of dots for dense continuous priors;
   never silently bypass the explicit current rule. Obtain one method-lane assignment.
2. Restore and provenance-check shared cached feature stack without committing
   large/private data; establish organizer licensing and permitted use.
3. Use shared buffered segment holdout and fold-visible catalogue features;
   run each raw-feature withheld-positive canary, then pooled paired spatial DTI
   and 95% CI versus same-fold incumbent. Stop after three experiments/two hours.
4. Only after uniqueness and science gates pass, generate genuinely new TIFF
   using the shared writer, validate read-back, expose approved download and hand
   promotion to the separate selector within authenticated weekly allowance.

The top-prize goal is not achieved by this corrective review. The concrete outcome
is an auditable negative artifact and removal of unsafe authorization paths.
