# GEMSDOE81 — New-lane hypotheses (session arena/db89212c, 2026-10-21)

Starting point re-read per AGENTS.md: README.md, docs/research/review.md,
evidence/run-card.json (preflight STOP), evidence/run_card.json (ASB, verdict
negative, HOLDOUT-DTI v81.1 0.0831 < d28 control 0.0992). The merged ASB lane
(scarp-pair x basement-step) is **taken**; this session must not re-run it.
Irregularity IR-81-DENSE (flagged, not silently resolved): the literal >0
reading of the 70%-within-3px rule against the dense 17GEMSDOE continuous
witness (positive on 100% of footprint) rejects every nonempty candidate
(evidence/preflight.json). The merged ASB candidate operationalised "dots"
against the **binary** registry rasters (winner h33-2-b2, d28). This session
follows that merged precedent, measures against winner + d28 + ASB binary
rasters, and leaves the final interpretation to the selector step. Promotion
to a weekly slot is NOT decided here.

## Why 0.2778 won (verified from GEMSDOE32 audit + this repo's science page)
h33-h33-2-b2 = the 0.2708 dotted base with every dot <=2px from the published
catalogue deleted (44,090 -> 37,654 dots). Under pooled DTI (alpha 0.2,
beta 0.8, 300 m triangular kernel) dots on/near already-catalogued faults earn
~no credit toward *undiscovered* test faults but pay false-positive mass, so
pruning raises DTI. Dotted (spacing ~2.8px ~= kernel radius) beats continuous
ridges (h19-5 0.1922 -> 0.2600 dotted) because one dot covers a 300 m kernel
disc; extra density is redundant FP mass. Emission efficiency, not a better
geophysical surface, explains most of the ordering. To beat 0.2778 we need a
surface with genuinely different off-catalogue support, emitted the same
efficient way (poisson 2.8px, buffer 2px, N in the 37.7k-44.1k band), and it
must beat the d28 control on the *same* hide-and-recover instrument first.

## Candidates (all label-free rank surfaces; layers already mirrored, no new external data)

| Rank (pre-data, expected DTI/cost) | ID | Layers | Physical signature | Why it catches a catalogue-missing fault | Named non-fault mimic | Difference from this repo (ASB) |
|---|---|---|---|---|---|---|
| 1 | RXF | geodawn_extensions_u8 ratio bands (Th/K, U/K, U/Th) + training_features RTP/TMI | gradmag of log radioelement ratios (geometric mean of ranks) x gradmag RTP | Fault juxtaposis/alteration changes K-Th-U ratios and magnetic basement across the fault even where alluvium erases the scarp; ratios normalise total-count/regolith effects | Alluvial-fan provenance boundary / lithologic contact with no fault offset | ASB uses 1 m lidar lapneg*lappos and grad(depth_to_basement),grad(conductivity); RXF uses no lidar, no basement, no conductivity |
| 2 | GMD | training_features iso_grav_anom + RTP | rank(gradmag gravity) x (1 - rank(gradmag RTP)) discordance, and concordant variant sqrt(rank*rank) as control arm | A fault offsetting dense but weakly-magnetic basement/sediment gives a gravity step with no magnetic step; such faults are exactly those missed by magnetic lineament mapping | Basin-margin hinge / sedimentary thickness change | No gravity in ASB; discordance (anti-coincidence) is the opposite algebra to ASB's coincidence product |
| 3 | PCD | training_features detrended elevation (band 12) | plan-curvature zero-crossing density + slope-break (gradmag of slope), gated to low-slope piedmont | 100 m-scale piedmont fault scarps/alluvial-fan offsets persist as slope breaks below 1 m-lidar scarp amplitude thresholds | Terrace riser / paleo-shoreline / fan-lobe boundary | ASB's geomorphology is 1 m lidar laplacian pair; PCD is 100 m DEM curvature, disjoint input stack |
| 4 | XPD | training_features RTP + iso_grav_anom | cross-strike profile displacement: local cross-correlation shift between adjacent parallel profiles; consistent signed shift = candidate | Buried lateral displacement survives scarp erosion (review.md rank-1 conditional hypothesis) | Intrusive contact, survey interpolation seam | Targets displacement, not edge amplitude; highest implementation cost, deferred unless 1-3 fail canary |

External data check: none of 1-3 needs new data (mirrors pinned in
registry/data_manifest.json: USGS GeoDAWN DOI 10.5066/P93LGLVQ derivatives +
competition feature stack). XPD also needs only mirrored bands.

## Validation plan (<=3 experiments, budget rule)
E1 Canary: AUC of each candidate transform alone vs catalogue (sampled,
gems81.holdout.auc_score). AUC>0.90 = leakage stop. Cheap rank ordering.
E2 Holdout: gems81 hide-and-recover v81.1 (whole 8-connected components,
2 draws, visible masked pixel-exactly, catalogue exclusion derived from
visible only per draw), pooled DTI, top surface(s) vs rebuilt ASB surface and
d28-dot control at identical emitter (poisson 2.8px, buf 2px, N 37654/44090).
E3 Final: emit best config on full catalogue, registry rank-corr + 3px-dot
overlap vs winner/d28/ASB (stop if >0.90 or >0.70), fail-closed writer +
read-back validator, unique name, <=140-char note, JSON run card.
Verdict promote ONLY if E2 beats the d28 same-instrument control (0.0992 from
ASB session, to be re-measured here); otherwise verdict negative and the site
must say NOT OK to submit despite format validity. No score >0.2778 is ever
claimed from holdout numbers (0.2778/0.4413 are organiser/leaderboard values,
labelled ORGANIZER-CONFIRMED / leaderboard observation, never mixed with
HOLDOUT-DTI).
