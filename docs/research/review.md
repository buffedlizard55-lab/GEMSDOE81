# Scientific and repository review — 2026-10-21

## Decision first

**DO NOT SUBMIT. No new TIF is authorized.** This is a negative deliverable,
not a successful generation claim. A prior parallel-session ASB candidate existed
in the inherited tree. The shared local validator passes its format checks; under
the literal support definition `finite & value > 0`, its exact final-dot overlap
against the pinned dense witness is 1.0, above the 0.70 stop. The candidate was
removed from the current Pages download tree. Its pre-emission surface was not
retained, and its prior two-draw holdout range is not a 95% CI from the pinned
shared evaluator.

**Important protocol ambiguity:** the pinned template also contains
`two_phase_summary`, which classifies a full-footprint positive raster as a
`continuous_surface` and says such an overlap firing is not itself evidence of
duplication; it reserves dot-overlap comparison for `dot_field` rasters. The user
protocol does not define whether a dense probability surface counts as a registry
raster's “dots”. This release does not silently choose the exemption or modify the
shared template: it logs the literal 100% overlap as a stop, but does not claim
that every conceivable like-for-like interpretation makes any nonempty prediction
impossible. The inherited candidate is still not promotable: no lane was assigned,
its raw surface and valid shared holdout/95% CI are missing, and no full dot-field
registry scan was performed. No new candidate surface or geological experiment
was built in this turn, and no weekly slot was used.

## Scope and prior sessions

The starting commit contains only `README.md` (11 bytes). The user's statement
that training is blocked *only* by data placement does not describe this checkout.
There was no previous-session pipeline at the starting commit. During this run,
concurrent PR #1 merged a research-only site into main. It was integrated without
discarding its notes: superseded material is retained under
`docs/archive/first-review/`, with current-status pointers at its old entry paths.
It added no model or data pipeline and does not change the measured stop. A later
parallel-session merge had added an ASB raster and a page incorrectly declaring it
safe to submit. The current review re-audited that inherited raster, recorded the
format/overlap results in `evidence/legacy-candidate-audit.json`, removed the
misleading download from the current site tree, and retired the private evaluator,
holdout, and writer modules. The source-history file is not treated as a current
candidate or a valid holdout result.
Read-only review sources:

- [GEMSDOE32 pinned tree](https://github.com/buffedlizard55-lab/GEMSDOE32/tree/f62038b54dcb7767d4d997f80b033cdc3d42bef9): H33 code, build receipts, research and artifact.
- [GEMSDOE77 pinned tree](https://github.com/buffedlizard55-lab/GEMSDOE77/tree/6c363745d864f01d47b9d2cba5da8857953e93d0): extensive family lane registry, prior saturation reports and data manifest. Its previous conclusions were treated as leads, not new measurements.
- [Shared template](https://github.com/buffedlizard55-lab/60GEMSDOE/tree/b99591eede63c6d45c8a896255b8cd34824fa00b/src/gems57): fetched byte-for-byte, SHA-pinned in `registry/template_pin.json`; the vendor copy remains unmodified. The inherited `src/gems81` private metric, holdout, and writer copies have been removed; only legacy ASB surface/emission source remains, unused by active submission commands.
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

The earlier 2026-10-21 source pass recorded a public-leaderboard value of 0.4413
for xiaofanhu (**OFFICIAL-LEADERBOARD-OBSERVATION**, not a receipt linking our
bytes to a score); it was not refreshed during this re-audit.
The prompt's 0.3195 is not the current leading value in that observation.

## Ranked hypotheses — proposals only, BEFORE implementation

Ranks are qualitative judgements about *possible* holdout-DTI improvement per cost,
**not projected scores or measured results**. None is claimed novel across all family
repositories: that requires a complete lane audit. The four proposals are new relative
to the first-review checkout, but prior-family novelty is unverified. Cached organizer
feature availability has **not** been established in this checkout; each proposal is
conditional, not a viable tested candidate. The top-ranked option is only a proposal
for after the shared stop is resolved and a method lane is assigned; no experiment is
authorized by this document.

| Rank / qualitative expected DTI improvement and implementation cost | Hypothesis, exact layers and targeted signature | Why it might reveal a missing fault rather than a mapped one | Named non-fault mimic / difference from reviewed work |
|---|---|---|---|
| First / expected holdout-DTI gain: moderate but uncertain; cost: medium | **Cross-strike profile displacement:** `rtp`, `iso_grav_anom`, `cond_surf`; estimate lateral profile shifts across a candidate discontinuity by normalized cross-correlation of adjacent parallel profiles, require a consistent signed displacement over several windows. | Buried displacement can survive even when the surface scarp is erased. | Intrusive lithologic contacts and interpolation seams. Targets displacement of profiles, not H33 ridge thinning or the reviewed magnetic gradient-worm amplitude. Family-wide novelty unverified. |
| Second / expected holdout-DTI gain: low-to-moderate; cost: medium | **Conductive-base flexure with magnetic continuity break:** `depth_to_base_surf`, `cond_surf`, `rtp`; signed second derivatives of conductive-base depth, gated by a change in magnetic profile phase across the flexure. | A buried barrier/conduit boundary may perturb conductive stratigraphy without a mapped Quaternary scarp. | Saline basin margins and inverted-model regularization. This tests a flexure/phase relation rather than a scalar product of edge magnitudes. Existing template physics lanes need a collision audit. |
| Third / expected holdout-DTI gain: plausible but high-variance; cost: high | **Paired catchment piercing points:** elevation/DEM and slope; flow-routing tributary heads and valley mouths on opposite sides of a proposed line, require consistent signed lateral offsets in multiple independent catchments. | Lateral fault motion can offset drainage without a continuous preserved scarp. | Stream capture, alluvial avulsion and DEM artifacts. Different from GEMSDOE32's collinear valley-chain hypothesis: the observable is repeated displacement, not straightness. Coarse detrended elevation may be insufficient; high-resolution official DEM would need an availability check before upgrading viability. |
| Fourth / expected holdout-DTI gain: low/uncertain until novelty is established; cost: medium | **Scale-asymmetric magnetic profile truncation:** `rtp`, `tmi`, `mag_anom`; compare left/right autocorrelation lengths along local strike across candidate boundaries, require truncation stable under smoothing but not aligned with survey seams. | Fault juxtaposition can terminate a magnetic fabric without producing a strong ridge. | Volcanic unit boundaries and survey-leveling errors. Unlike amplitude/edge worms, this tests texture termination; texture lanes already exist and novelty is unresolved. |

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

1. **Universal witness under one support definition / shared semantic conflict:**
   the pinned prior is positive at every sample-footprint pixel. See
   `evidence/preflight.json`. If every positive pixel is treated as a dot, it
   covers every allowed location in its three-pixel halo and blocks every
   nonempty candidate. However, the same pinned template's `two_phase_summary`
   treats a dense support as a continuous surface and says its overlap firing is
   not duplication evidence; only dot fields receive like-for-like dot overlap.
   The user protocol leaves “registry raster's dots” ambiguous. Keep this release
   fail-closed and resolve the semantics in the shared protocol/template, not a
   private fork. The negative is a policy stop, not proof that all interpretations
   forbid every possible nonempty raster.
2. **Inherited ASB candidate is not safe to submit:** the previous page said “OK TO
   DOWNLOAD & SUBMIT”, but only compared its raster with selected H33/d28 examples.
   Under the literal finite-positive support definition, the exact audit finds
   final-dot overlap 1.0 against the pinned dense witness, above the 0.70 limit;
   the candidate is withdrawn from the current Pages tree. Because the pinned
   template classifies that witness as a continuous surface, this is not an
   interpretation-independent duplicate finding. Its local format checks pass,
   but uniqueness and acceptance are not cleared.
   Its pre-emission surface bytes are absent, so its surface rank correlation cannot
   be reconstructed; a candidate-independent pre-placement proof already blocks it.
3. **Legacy model-evaluation record is not protocol-compliant:** the imported
   receipt's HOLDOUT-DTI values were produced by private v81.1 code with two draws;
   its two-draw min/max is not a 95% CI. Its AUCs were not produced on the required
   blocked holdout. A historical H33 comparison also uses a raster pruned against
   the full catalogue, including hidden labels, so it is not a valid hide-and-recover
   control. Do not promote or compare these values to organizer scores. The private
   metric, holdout and writer modules were removed; active evaluation uses pinned
   `vendor/gems57` only.
4. **Historical score provenance:** the H33 page's 0.2778 is USER-REPORTED in the
   supplied context, not ORGANIZER-CONFIRMED by a submission-page receipt; the
   pinned H33 build receipt says UNSCORED. The prior parallel candidate card's
   “ORGANIZER-CONFIRMED” label was incorrect and has been removed. The 0.4413
   public-board number is a dated OFFICIAL-LEADERBOARD-OBSERVATION, not a receipt
   for a particular raster; the prompt's 0.3195 is user-reported and may be stale.
5. **No assigned lane.** The method paragraph referenced by the protocol is absent.
   Do not infer authorization from the repository number or revive ASB, H81, or
   another prior lane.
6. **No organizer-authenticated data or submission receipts.** SHA integrity of
   owner mirrors does not establish official origin, licensing, AOI coverage, or
   acceptance. The full cached feature stack is absent; data placement alone does
   not make this checkout's model pipeline ready. GPU need is not established for
   the proposed CPU transforms.
7. **Competition rules and cap:** the rules PDF was not fully audited here, and the
   authenticated submission-page weekly allowance is unknown. No number is
   invented; no selector or competition submission is automated.
8. **Range-error diagnosis:** the failed upload itself was not supplied. NaN,
   infinity, nodata sentinels, or values outside [0,1] are possible causes, not a
   diagnosis. The inherited ASB candidate passes the shared local range checks;
   that does not explain the separate rejection or guarantee portal acceptance.
9. **Freshness:** official web observations are dated snapshots, not a live feed.
   CI reruns mathematical and input checks; it does not claim daily leaderboard
   retrieval. Future source monitoring must retain timestamps and errors.

### Three passes in this session

- Pass 1: read the README and current review, restored the three hash-pinned audit
  inputs, verified the shared-template hashes, reproduced the pre-placement stop,
  re-audited H33 bytes, and ran the existing tests. This exposed an inherited site
  page that incorrectly advertised an ASB raster as safe to submit.
- Pass 2: validated the inherited raster with the shared validator; independently
  measured final-dot overlap under the literal support definition, documented the
  shared-template semantic conflict, corrected score provenance; removed the unsafe
  TIF from the published tree; retired private evaluator/holdout/
  writer copies and the side-effecting candidate generator; added fail-closed checks.
- Pass 3: regenerate the status site and run tests, preflight, candidate audit report
  consistency, source/local-link checks, compile checks, and `git diff --check`. No
  new candidate, experiment, holdout score, or weekly slot is authorized.

Reproduction commands and results are in README and `evidence/verification.json`.

### Historical integration and current re-audit — 2026-10-21

The earlier integration brought in the pinned shared tools, one registry witness,
and a reproducible preflight. At that point the negative page said no candidate
existed. A later parallel merge added the ASB TIF and a page that incorrectly
labeled it safe to submit; its receipt did not check the dense witness.

In this re-audit, the three hash-pinned inputs were restored and `scripts/audit.py`
again returned exit 2 / `STOP_LITERAL_SUPPORT_OVERLAP`. The inherited candidate's local
format checks pass, but the exact final-dot overlap is 1.0 against the pinned witness
under the literal positive-support definition; the pinned template's continuous-
surface reading leaves dot-field semantics unresolved. See
`evidence/legacy-candidate-audit.json`. Its raw pre-emission surface is absent.
The TIF and misleading receipt were removed from the current Pages tree; the
candidate's name and SHA remain in the run card as a historical negative result.
The prior private metric/holdout/writer modules and unsafe generator entry points
were retired. `scripts/audit_reference.py` rechecked H33 bytes for learning only;
its site-reported value remains unconfirmed. No new experiment, current HOLDOUT-DTI,
submission upload, or slot use occurred. External-source review remains landing-
page-level only: no external dataset bytes or target-area coverage were verified.
