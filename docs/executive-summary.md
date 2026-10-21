# Executive summary and submission guide

## Release status — not ready

**No candidate TIFF exists in this checkout.** **OK TO DOWNLOAD: NO FILE. OK TO SUBMIT: NO.** The local project is only a README; the assigned lane, shared feature cache, shared evaluator/writer, registry, competition data, and sample grid are absent. Do not upload a file from another GEMSDOE site or create a submission slot based on a format-only check.

The top-level [project site](../index.html) repeats this status. When a candidate is cleared by the experiment and selector gates, this page should be updated with the exact file, SHA-256, format receipt, HOLDOUT-DTI evidence, uniqueness result, submission name, and short note.

## How to submit a promoted file

The upload actions below apply **only** after the site says **OK TO SUBMIT: YES** for an exact, hash-identified candidate. That condition is not met today.

1. Open the [official GEMS competition page](https://www.drivendata.org/competitions/306/competition-doe-gems/) and sign in to the account enrolled in the competition.
2. From this project site, download the file explicitly marked **OK TO SUBMIT: YES**. Confirm the filename and SHA-256 match the site's receipt. Do not use a research-only, negative, or old artifact.
3. Open the competition's **Submit** form. Select the single-band `.tif` file, or a `.zip` containing exactly one GeoTIFF, as accepted by the submission form. The official [problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) specifies one float32 layer on the training grid.
4. Enter the unique submission name printed on the project site. In **Note (optional)**, paste the ≤140-character note printed there; do not invent a note that claims an unverified method or score.
5. Submit only if the competition page shows a remaining slot and the separate selector has authorized this exact artifact. The project does not select or spend slots automatically.
6. Save the actual submission-page receipt, including the submitted filename, timestamp, result/score, and submission ID. Only that receipt can support an `ORGANIZER-CONFIRMED` label for this exact artifact.

## Required file checks before a future download

The official format rules require the submission to match the training grid (CRS, resolution, bounds, and transform), use one float32 band, keep predicted values in `[0,1]`, and represent cells outside the data bounds as null/NaN. The checker must reopen the final bytes from disk and verify these properties, not just the in-memory array. The full competition format is on the [official problem page](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/#submission-format).

The prior portal message **“Predicted values must be in range [0, 1]”** alone does not reveal whether the cause was a true out-of-range pixel, a nodata sentinel included in the submitted footprint, an incorrect file/band, or another validator issue. The rejected file is not present in this repository, so the cause is unknown here. The only responsible repair is to inspect the exact rejected bytes and run a full pixel scan and grid comparison; do not claim a fix without that evidence.

## Why there is no download link today

This is a deliberate fail-closed decision. The run card records no method, no score, no registry comparison, no raster hash, and no validator result because none can be produced from this checkout. A synthetic or copied TIFF would not satisfy the competition objective or the parallel-run uniqueness rule. A current, audited negative/blocked status is safer than an invalid file that could consume a weekly slot.
