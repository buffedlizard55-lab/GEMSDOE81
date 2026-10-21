# Forensic review: the H33-2-B2 raster and the reported 0.2778

**Evidence boundary:** this is a source review, not a new holdout evaluation. No H33 raster was copied into this checkout, no local pixel-level audit was run, and no submission-page receipt for the H33 artifact was available. Accordingly, the user's `0.2778` is **user-reported and unverified here**; it is not HOLDOUT-DTI and cannot be called ORGANIZER-CONFIRMED under the project's receipt rule.

## What the authoritative task metric rewards

The official [problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/#performance-metric) defines distance-weighted Tversky with a triangular kernel of 300 m support (three 100 m pixels), α=0.2 for false positives, and β=0.8 for false negatives. For each truth pixel, the best nearby prediction gets credit; prediction mass outside any truth pixel's 300 m kernel is penalized. The official example gives partial credit for a near miss. This means a sparse, correctly placed trace can outperform a thick trace that spends many predictions on already-covered locations. It does **not** mean that a lineament is a fault or that high DTI alone proves a geothermal vent.

## What the original GEMSDOE32 page actually says

The [GEMSDOE32 page](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html), inspected on 2026-10-21, advertised `gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros.tif` as its primary candidate. Its own audit lists 37,654 positive pixels, zero on-catalogue positives, a single float32 band, EPSG:32611, and a shape of 3,730 × 3,292. These are **artifact-format/provenance claims from that repository's audit**, not a new measurement in this checkout.

Crucially, the same page says the live-anchored value 0.2747 is a **model projection, not a score**, and says **“NO ORGANISER SCORE EXISTS”** for its artifacts. The original page's primary file is therefore not evidence of an organizer-confirmed 0.2778 result. The 0.2778 value appears in the supplied owner brief, but no submission receipt tying that value to this exact file was provided. This discrepancy is logged in [`../irregularities.md`](../irregularities.md).

A later public [GEMSDOE77 forensic report](https://github.com/buffedlizard55-lab/GEMSDOE77/blob/main/reports/why_02778.md) says its authors compared bytes and found the H33 dots on a previously used H19-5 ridge support after near-catalogue pruning. That is useful secondary analysis, but this checkout did not independently reproduce its hash or spatial comparisons. Treat it as a linked, external research report—not as an official score receipt.

## Plausible mechanism if the reported ranking is accurate

The candidate lineage described by GEMSDOE32 is an emission-rule change on an existing ridge-based dot field: start with a previously used baseline, delete dots close to the mapped catalogue (the `B=2`/two-pixel flank prune), and retain the remaining sparse support. The plausible statistical gain is not a new geological discovery by itself. It comes from changing the precision–recall tradeoff under the metric:

- Removing predictions near the public catalogue may reduce wasted mass where those locations are unlikely to be new test faults.
- Sparse dots reduce redundant mass where nearby predictions would all earn nearly the same maximum credit for a single truth pixel.
- The 300 m kernel preserves partial credit when a retained dot is near, but not exactly on, a hidden fault.
- Because β is larger than α, missed hidden-fault pixels are relatively costly, so modest false-positive mass can be acceptable if it covers additional faults.

The non-fault alternatives are important: a terrain ridge or scarp may follow lithologic boundaries, erosional surfaces, drainage, or anthropogenic disturbance. The score can reward proximity without identifying the actual fault plane; a hidden-test score, if real, would establish metric performance on that split, not a causal geothermal interpretation.

## Can GEMSDOE81 beat it?

**Not demonstrated.** In principle, a better detector or emitter could score higher; the official metric and leaderboard permit scores above the value in the brief. However, the current official public leaderboard, read on 2026-10-21, showed a first-place entry of 0.4413. This is a **public leaderboard observation**, not a receipt for this project's file, not a private-test result, and not an authorization to imitate that entry. The user's 0.3195 figure is stale relative to that observed page.

This checkout cannot establish that GEMSDOE81 can beat 0.2778: there is no assigned lane paragraph, data, cached features, registry, evaluator, writer, holdout baseline, or candidate raster. No experiment or score was produced. A competitive answer requires a new surface that passes the novelty/duplicate screen and improves the shared blocked holdout; no trustworthy promise can be made from leaderboard context alone.

## Decision

**Negative / blocked, not a promoted candidate.** Do not copy the H33 TIFF. Do not label the user's 0.2778 as organizer-confirmed without its submission-page receipt. Continue with the provisional, source-backed research shortlist only after the missing lane and shared inputs are available. The session run card is [`../../evidence/run_card.json`](../../evidence/run_card.json).
