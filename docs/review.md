# Repository review — three-pass verification

Reviewed on 2026-10-21 on branch `arena/031d34fb-gemsdoe81`.

## Pass 1 — inventory and source review

- `git status --short --branch` showed the active branch and no existing modifications before work.
- `find . -maxdepth 4 -type f -not -path './.git/*'` returned only `README.md`.
- `git log -1` showed the checkout at the initial commit `e8b69dde87ad29bac860abf359f9d394af970423`.
- No `data/`, `.cache`, `registry/`, `scripts/`, `src/`, tests, package metadata, feature stack, template pin, evaluator, writer, sample grid, or TIF exists locally.
- Official DrivenData page 967 and the official public leaderboard were fetched. The metric and submission contract were checked against page text. Official USGS GeoDAWN, USGS/DOE geothermal, DOE GDR, and shared-repository source pages were reviewed; exact source links and limits are in [`sources.md`](sources.md).
- The original GEMSDOE32 page's score caveat was checked: it labels 0.2747 as a projection and says no organizer score existed for its artifacts at that time. No receipt for the user's 0.2778 attribution is present.

## Pass 2 — protocol and scientific-assumption review

- The supplied brief contains no uniquely identified method paragraph, so there is no assigned lane.
- Required inputs for a surface-level duplicate check, a buffered-segment holdout, a per-feature leakage canary, and a final writer/validator are absent.
- The historical score list includes user-supplied scores and sibling-site reports, not receipt-backed evidence for a GEMSDOE81 artifact. The official leaderboard is dynamic; the observation at this review differs from the brief's stated value.
- The reported portal error cannot be diagnosed from its text without the rejected bytes. The submission format and in-footprint range must be rechecked from disk.
- Result: do not create a speculative surface, copy an earlier raster, label a projection as a score, create a fake run, or touch a weekly slot.

## Pass 3 — deliverable and regression review

- Added a static, dependency-free project site with the download/submit status in its first viewport and a separate executive submission guide.
- Added a provenance-aware H33 analysis, ranked but explicitly provisional hypotheses, official-source register, irregularity log, and a JSON run card with null measurements rather than invented results.
- Verified that the site says no file is available and no upload is approved. No TIFF or zip was created.
- Added and ran `python3 scripts/check_site.py`: all five HTML pages, local links/anchors, release-card fields, fail-closed status, and the no-TIFF gate pass. `git diff --check` passes.
- Queried the GitHub Pages configuration: legacy publishing is configured from `main` at `/` and is public. The new site content has not yet been published/verified on the live URL; it will be available after the requested PR merge and Pages rebuild.
- This pass is a documentation/site review only. It is not a model validation or a competition score.

## Final decision

`negative` / `blocked_not_tested`. No HOLDOUT-DTI was measured; no 95% CI exists; no registry correlation/overlap was computed; no raster SHA-256 or TIFF validator output exists. The only supported next step is to resolve the lane and obtain the shared template plus its authorized data/cache/registry in a future session.
