# Irregularities and release blockers

Status date: 2026-10-21. Severity is about whether a scientific run or competition upload can proceed.

| ID | severity | observation | consequence / action |
|---|---|---|---|
| IR-81-001 | release blocker | Initial repository inventory contained only `README.md`; this review added docs/site files, but there are still no scripts, tests, source modules, competition data, shared-template pin, feature cache, registry, or sample submission grid. | Cannot run the requested shared evaluation/writer or create a format-matched TIFF. Obtain the designated shared template and authorized inputs before any experiment. |
| IR-81-002 | release blocker | The supplied prompt says the lane is “the single method paragraph below,” but no identifiable method paragraph is assigned. | Protocol prohibits selecting another method speculatively. No surface or candidate dots were generated. The owner must provide/confirm the lane in a future brief; this is not resolved by guessing. |
| IR-81-003 | score provenance | The user's prompt calls 0.3195 the current public high score, but the live official public leaderboard page read on 2026-10-21 displayed xiaofanhu at 0.4413. | 0.3195 is historical/stale at the observation time. Keep the live official link; do not copy a permanent static feed or infer private-test performance. The board observation is not a submission-page receipt for this project. |
| IR-81-004 | score attribution | The user's prompt attributes 0.2778 to H33-2-B2. The original GEMSDOE32 page says no organizer score existed for its artifacts and labels 0.2747 as a model projection. | 0.2778 is not authenticated by an exact submission-page receipt in this checkout. Treat the attribution as unverified until a receipt links that exact artifact and score. |
| IR-81-005 | uniqueness blocker | There are no registry rasters or registry index in this repository. | Rank correlation and 3-pixel dot overlap cannot be computed on a candidate surface or final dots. Do not state uniqueness. |
| IR-81-006 | evaluation blocker | There is no shared `evaluate_holdout.py`, no shared `submission_writer.py`, no cached feature stack, and no local catalogue/labels. | No buffered segment hide-and-recover holdout, individual-feature leakage canary, pooled DTI, withheld-positive count, or CI can be measured. Do not write a score. |
| IR-81-007 | submission blocker | No TIFF, validation receipt, candidate name, or note exists. | The site intentionally has no download link and states `OK TO DOWNLOAD: NO FILE` / `OK TO SUBMIT: NO`. |
| IR-81-008 | unresolved portal error | The only supplied evidence is the text “Predicted values must be in range [0, 1]”; the rejected TIFF is absent. | That message alone does not isolate the offending pixels or nodata encoding. No fix is claimed; inspect the exact bytes when they are available. |
| IR-81-009 | data access | Official competition data downloads are login-gated, and the current checkout has no account-authenticated data. Public external source pages exist, but their payloads were not downloaded in this environment. | Do not use unverified mirrors or claim a source is locally usable. Track exact data source, terms, AOI coverage, byte hash, and attribution before adding it. |
| IR-81-010 | scope / provenance | The long family score list in the user prompt was not independently audited item-by-item in this session; entries are not submission receipts unless an exact receipt is available. | Do not use the full list as a verified score ledger. This review checked the H33 source caveat and the current official public board only. |

## Release decision

**Negative / blocked. No experiment, TIFF, or slot selection.** This is a protocol decision based on missing prerequisites, not a negative HOLDOUT-DTI measurement. See [`../evidence/run_card.json`](../evidence/run_card.json) and [`review.md`](review.md).
