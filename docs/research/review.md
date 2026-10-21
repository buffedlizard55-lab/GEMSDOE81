> **Historical review, superseded where inconsistent.** This document predates
> the parallel ASB artifact integration. The TIFF now exists as a negative research
> artifact; no new TIFF was generated in the corrective review. Use the
> [current corrective review](session-review.md) and
> [authoritative card](../evidence/run-card.json) for current status. Statements
> below about an empty initial checkout or absent candidate describe that earlier
> review, not the present repository. No organizer performance receipt exists.

# Scientific and repository review — 2026-10-21

## Decision first

**DO NOT SUBMIT. There is no authorized new TIF.** This is a negative deliverable,
not a successful generation claim. The protocol's literal uniqueness rule is
unsatisfiable for a nonempty in-footprint prediction against the verified dense
registry witness. Generating a fake, empty, copied, or relabelled TIF would not
meet the brief. No new candidate surface was constructed, no experiment was run,
and no weekly slot was used. The proof applies before placement and to all final
dot sets. A complete registry scan cannot overturn a single sufficient rejection
witness; we do not claim such a scan was performed.

## Scope and prior sessions

The starting commit contains only `README.md` (11 bytes). The user's statement
that training is blocked *only* by data placement does not describe this checkout.
There was no previous-session pipeline at the starting commit. During this run,
concurrent PR #1 merged a research-only site into main. It was integrated without
discarding its notes: superseded material is retained under
`docs/archive/first-review/`, with current-status pointers at its old entry paths.
It added no model or data pipeline and does not change the measured stop.
Read-only review sources:

- [GEMSDOE32 pinned tree](https://github.com/buffedlizard55-lab/GEMSDOE32/tree/f62038b54dcb7767d4d997f80b033cdc3d42bef9): H33 code, build receipts, research and artifact.
- [GEMSDOE77 pinned tree](https://github.com/buffedlizard55-lab/GEMSDOE77/tree/6c363745d864f01d47b9d2cba5da8857953e93d0): extensive family lane registry, prior saturation reports and data manifest. Its previous conclusions were treated as leads, not new measurements.
- [Shared template](https://github.com/buffedlizard55-lab/60GEMSDOE/tree/b99591eede63c6d45c8a896255b8cd34824fa00b/src/gems57): fetched byte-for-byte, SHA-pinned in `registry/template_pin.json`. No private evaluator/writer fork.
- LEARNGEMSDOE, GEMSDOE73 and GEMSDOE80 GitHub trees inspected for tooling; this is **not** a line-by-line review of every family repository or website.

The assigned method paragraph is absent. H81 is already used for slip-cone
continuation in GEMSDOE77; repository number 81 is **not** permission to reopen
that lane. This session is an infrastructure/preflight review, not a new lane.

## What actually explains H33?

[H33's pinned build receipt](https://github.com/buffedlizard55-lab/GEMSDOE32/blob/f62038b54dcb7767d4d997f80b033cdc3d42bef9/docs/downloads/gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-audit.json)
describes deleting dots within two pixels of the mapped catalogue from an existing
dotted baseline. We independently read its TIF: 37,654 binary positive pixels,
all finite and in [0,1], no positive catalogue or out-of-footprint pixels, minimum
catalogue distance sqrt(5) pixels, median nearest-dot spacing 3 pixels.
These are **REFERENCE-BYTE-MEASUREMENTS**, not performance scores.

The plausible mechanism is **emission efficiency**, not evidence that a new
geophysical model discovered more faults. Dots spaced near the kernel radius can
cover a line with less redundant prediction mass than a solid rasterized ridge.
Pruning mapped-fault-adjacent dots may remove mass that does not help recover
initial-round *new* faults. Whether it actually improves unseen faults depends on
hidden labels; mapped faults can have parallel unmapped strands, so a blanket
collar can also delete useful predictions. It can be worse for the final round,
which uses the expanded all-fault label set.

The official max-cover DTI does **not** generally justify the shortcut “each new
dot adds exactly alpha to the denominator.” For a candidate addition, let u be
the increase in total covered truth and v its added distance-weighted false-positive
mass. Then FN decreases by u and the denominator increases by
(1-beta)u + alpha*v. The addition improves DTI D iff
`u > D*((1-beta)*u + alpha*v)` (ignoring only the negligible epsilon).
Here alpha = 1-beta = 0.2. Neighbouring predictions compete through a maximum,
so u can be zero for a redundant dot. This is why density and placement matter;
it is not a formula to infer hidden truth from public scores.

**Attribution limit:** 0.2778 is USER-REPORTED, not ORGANIZER-CONFIRMED. The pinned
build receipt explicitly says UNSCORED and includes a projection, not a submission-page
receipt. Its legacy holdout fields mix summaries and cannot be relabelled as a
current pooled HOLDOUT-DTI with a confidence interval. We cannot establish causal
superiority, or promise to exceed that value, from those artifacts.

The public leaderboard retrieved on 2026-10-21 shows 0.4413 for xiaofanhu
(**OFFICIAL-LEADERBOARD-OBSERVATION**, not a receipt linking our bytes to a score).
The prompt's 0.3195 is not the current leading value in that observation.

## Ranked hypotheses — proposals only, BEFORE implementation

Ranks are qualitative priority judgments, **not projected scores**. None is claimed
novel across all family repositories: that requires a complete lane audit. All are
new relative to this initially empty checkout. No new external data is required in
principle; cached organizer feature availability has **not** been established in
this checkout. These are conditional proposals, not viable tested candidates.
Only the first should be considered after the shared stop condition is resolved
and a narrow lane is assigned; no experiments are authorized by this document.

| Rank / qualitative expected value vs cost | Hypothesis, layers and exact signature | Why it might reveal a missing fault | Non-fault mimic / difference from reviewed work |
|---|---|---|---|
| First / medium cost; strongest expected value per cost, conditional | **Cross-strike profile displacement:** `rtp`, `iso_grav_anom`, `cond_surf`; estimate lateral profile shifts across a candidate discontinuity by normalized cross-correlation of adjacent parallel profiles, require a consistent signed displacement over several windows. | Buried displacement can survive even when the surface scarp is erased. | Intrusive lithologic contacts and interpolation seams. Targets displacement of profiles, not H33 ridge thinning or the reviewed magnetic gradient-worm amplitude. Family-wide novelty unverified. |
| Second / medium cost; moderate expected value and implementation burden | **Conductive-base flexure with magnetic continuity break:** `depth_to_base_surf`, `cond_surf`, `rtp`; signed second derivatives of conductive-base depth, gated by a change in magnetic profile phase across the flexure. | A buried barrier/conduit boundary may perturb conductive stratigraphy without a mapped Quaternary scarp. | Saline basin margins and inverted-model regularization. This tests a flexure/phase relation rather than a scalar product of edge magnitudes. Existing template physics lanes need a collision audit. |
| Third / high cost; plausible value, weaker cost-adjusted priority | **Paired catchment piercing points:** elevation/DEM and slope; flow-routing tributary heads and valley mouths on opposite sides of a proposed line, require consistent signed lateral offsets in multiple independent catchments. | Lateral fault motion can offset drainage without a continuous preserved scarp. | Stream capture, alluvial avulsion and DEM artifacts. Different from GEMSDOE32's collinear valley-chain hypothesis: the observable is repeated displacement, not straightness. Coarse detrended elevation may be insufficient; high-resolution official DEM would need an availability check before upgrading viability. |
| Fourth / medium cost; lower expected value until novelty is established | **Scale-asymmetric magnetic profile truncation:** `rtp`, `tmi`, `mag_anom`; compare left/right autocorrelation lengths along local strike across candidate boundaries, require truncation stable under smoothing but not aligned with survey seams. | Fault juxtaposition can terminate a magnetic fabric without producing a strong ridge. | Volcanic unit boundaries and survey-leveling errors. Unlike amplitude/edge worms, this tests texture termination; texture lanes already exist and novelty is unresolved. |

The named magnetic/electrical bands are from the organizer-described competition feature stack; the official problem page is public, but the competition data page is login-gated. The local manifest pins owner-supplied mirrors for integrity only, not organizer authentication or redistribution permission. The catchment proposal additionally needs DEM/slope; high-resolution official DEM coverage must be checked before it could be called viable. A separate [external-source/access screen](external-source-screen.md) records geothermal, ASTER, 3DEP, Landsat, and Sentinel-1 leads. Some official landing pages were reachable, while the 3DEP page was only nominated from the owner-supplied manifest; target-area coverage and data bytes were not verified, so none is promoted as an obtainable/viable input.

These are **mechanistic conjectures**, not established fault indicators or claims of
geothermal vents. The target is fault structure; a fault prediction is not proof
of an active vent, permeability, temperature or commercially useful resource.

## Validation protocol after unblocking

Use the shared cached non-catalogue feature stack; do not retrain on historical
submission rasters. Hide whole fault segments with a buffer. Derive every
catalogue feature from only visible faults separately per fold. Mask visible
faults pixel-exactly. Do not treat the `labels.tif` mirror as independent hidden
truth: its SHA equals `existing_faults.tif` in the reviewed manifest.

Run each input feature alone on withheld positives and matched negatives; AUC
above 0.90 stops for a leakage investigation (also inspect inverse AUC).
Compute pooled HOLDOUT-DTI with shared `evaluate_holdout.py`, alpha 0.2, beta 0.8,
300 m triangular kernel. Publish evaluator version, actual withheld count and
spatial-block-bootstrap 95% CI. Re-evaluate the incumbent on exactly the same
folds; no compatible best is established here. Require paired improvement before
promotion. Run the literal registry gates on the surface before placement and on
final dots. Limit to three experiments or two hours. No selector or weekly slot
is consumed by this review. Holdout success would not guarantee public/private
leaderboard improvement under catalogue-to-new-fault distribution shift.

## Irregularities and next work

1. **Universal duplicate witness:** pinned prior is positive at every footprint
   pixel. See `evidence/preflight.json`. Correction from the subsequent code review: the pinned shared uniqueness module
   explicitly has **no density exemption**. The earlier claim that it contained
   one was wrong; `vendor/gems57/uniqueness.py` and its SHA pin verify the literal rule.
   Resolve semantics in the shared protocol first, not a private fork.
2. **No identifiable lane assignment.** Do not open another H81 lane by accident.
3. **No organizer-authenticated data or submission receipts.** SHA integrity of
   owner mirrors does not establish official origin, licensing, or acceptance.
4. **No cached feature stack here.** The three small audit inputs are not a
   complete training-data restore. GPU is not established as necessary for these
   CPU hypotheses; the old GPU pipeline claim does not apply to this repo.
5. **Rule and feedback cap:** PDF source was opened but not fully audited in this
   session. The authenticated submission-page remaining weekly cap is unknown;
   no number is invented. No competition submission automation is implemented.
6. **Historical range error:** the failed file itself was not supplied. NaN,
   infinity, nodata sentinels, or values outside [0,1] are possible causes, not
   diagnoses. The inspected H33 zeros file does not exhibit that range error.
7. **Freshness:** official web observations are dated snapshots, not a live feed.
   CI reruns mathematical/input checks; it does not claim daily leaderboard
   retrieval. Future source monitoring must retain timestamps and errors.

### Three passes

- Pass 1: restore pinned audit inputs, vendor unmodified shared code, recompute
  the pre-placement rejection proof and H33 byte properties; build docs and CI.
- Pass 2: test radius boundaries, empty supports, hash/grid mismatch and stale
  authorization; review the exact DTI marginal algebra and dense-prior exemption.
- Pass 3: rerun the tests and audits from pinned dependencies; verify website
  links, fail-closed download state, no generated candidate or unauthorized score
  claims, and explicit limitations before PR/merge.

Reproduction commands and results are in README and `evidence/verification.json`.

### Follow-up concurrent integration — 2026-10-21

After this review was first written, main advanced through PR #2 (`db03f65`) with the pinned shared tools, registry witness and reproducible preflight. This branch integrated that state instead of publishing a second competing site. We restored only the three hash-pinned audit inputs, reran `scripts/audit.py`, and reproduced exit 2 / `STOP_UNIVERSAL_DUPLICATE`; no candidate, geological experiment, leakage canary, or holdout was run. `scripts/audit_reference.py` rechecked the H33 raster bytes for learning only and still provides no performance score. The generated site now states `OK TO DOWNLOAD AS A COMPETITION SUBMISSION: NO FILE` and `OK TO SUBMIT: NO`; all 25 repository tests pass, including checks for in-page HTML fragments and current local Markdown links. A local HTTP smoke check returned the landing page, executive summary, source screen and preflight successfully. The additional official external-source screen is page-level only: no external dataset bytes or target-area coverage were verified.
