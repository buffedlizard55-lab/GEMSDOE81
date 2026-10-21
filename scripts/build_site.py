#!/usr/bin/env python3
"""Generate a fail-closed static site; never publish a negative candidate TIFF."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _guard_publication(card: dict, preflight: dict, candidate: dict) -> None:
    if card.get("authorized_to_download_and_submit") is not False:
        raise ValueError("This release must fail closed unless the card explicitly denies submission")
    if card.get("verdict") != "negative":
        raise ValueError("The negative-result site cannot publish a non-negative verdict")
    if preflight.get("decision") != "STOP_LITERAL_SUPPORT_OVERLAP":
        raise ValueError("Missing literal-support stop: recompute and review the preflight")
    if preflight.get("authorized_to_submit") is not False:
        raise ValueError("Preflight approval must remain false")
    if candidate.get("authorized_to_download_and_submit") is not False:
        raise ValueError("Legacy candidate audit must remain explicitly unauthorized")
    registry = candidate.get("registry", {})
    if not registry.get("duplicate_by_literal_overlap"):
        raise ValueError("Legacy candidate literal-overlap finding is missing")
    if registry.get("witness_representation", {}).get("kind") == "continuous_surface" and not registry.get("shared_template_two_phase_note"):
        raise ValueError("Dense-surface semantic ambiguity must be documented in the candidate audit")
    if candidate.get("candidate", {}).get("sha256") != card.get("raster_sha256"):
        raise ValueError("Run card and legacy candidate audit identify different raster bytes")
    if not candidate.get("validator", {}).get("all_checks_passed"):
        raise ValueError("Expected local format measurement is missing")
    blocked = [p for p in DOCS.rglob("*") if p.is_file() and p.suffix.lower() in {".tif", ".tiff", ".zip"}]
    if blocked:
        raise ValueError(f"Submission-like artifact must not be published from this negative site: {blocked[0]}")


def main() -> None:
    card = _load_json(ROOT / "evidence/run-card.json")
    preflight = _load_json(ROOT / "evidence/preflight.json")
    candidate = _load_json(ROOT / "evidence/legacy-candidate-audit.json")
    _guard_publication(card, preflight, candidate)

    evidence_dir = DOCS / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "preflight.json",
        "run-card.json",
        "reference_audit.json",
        "legacy-candidate-audit.json",
    ):
        (evidence_dir / name).write_text((ROOT / "evidence" / name).read_text())

    sources = _load_json(ROOT / "registry/sources.json")
    rows = "".join(
        "<tr>"
        f"<td><a href=\"{html.escape(s['url'], quote=True)}\">{html.escape(s['name'])}</a></td>"
        f"<td>{html.escape(s['status'])}</td>"
        f"<td>{html.escape(s['supports'])}</td>"
        "</tr>"
        for s in sources["sources"]
    )
    header = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>GEMSDOE81 · Submission audit</title>'
        '<link rel="stylesheet" href="style.css"><body><header>'
        '<a class="brand" href="index.html">GEMS<span>DOE81</span></a>'
        '<nav aria-label="Main navigation"><a href="executive-summary.html">How to submit</a>'
        '<a href="research/review.md">Research</a>'
        '<a href="https://github.com/buffedlizard55-lab/GEMSDOE81">Repository ↗</a></nav>'
        '</header><main>'
    )
    footer = (
        "</main><footer>Evidence over optimism. Own the outcome.<br>"
        "Reviewed 21 October 2026 · Dated snapshot, not a live leaderboard feed."
        "</footer></body></html>"
    )

    home = """<p class="eyebrow">FAULT MAPPING / AUDITED RESEARCH</p>
<h1>Do not submit a file from this release.</h1>
<p class="lead">This project studies unmapped geological faults. A fault prediction is not evidence of an active geothermal vent, permeability, temperature, or a viable resource.</p>
<p><a href="#sources">Jump to dated source audit ↓</a></p>
<section class="stop" aria-labelledby="status"><p class="eyebrow">CURRENT SUBMISSION STATUS</p>
<h2 id="status">DO NOT SUBMIT — no authorized TIF.</h2>
<div class="gate-status" role="status" aria-live="polite">
<p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: NO FILE</strong></p>
<p><strong>OK TO SUBMIT: NO — the literal registry-uniqueness gate fails.</strong></p></div>
<p>No new submission TIFF was generated. A prior-session ASB raster passed local format checks but its final dots have 100% overlap against the pinned dense witness under the literal positive-pixel support definition, above the 70% stop threshold. The file and misleading download link were removed from the current published tree.</p>
<p>Protocol ambiguity: the pinned template's <code>two_phase_summary</code> classifies this witness as a continuous surface and says its overlap firing is not itself duplicate evidence. The user protocol does not define whether dense support pixels count as a registry raster's “dots”. We do not silently invoke that exemption, so uniqueness is not cleared. The retained JSON audit is research evidence only, not a submission file.</p>
<button disabled>Submission TIF unavailable — protocol blocked</button>
<p><a class="button" href="evidence/run-card.json" download>Download negative run card ↓</a>
<a href="evidence/legacy-candidate-audit.json">View the inherited candidate audit →</a>
<a href="executive-summary.html">Submission instructions →</a></p></section>
<div class="metrics"><section><span>01</span><h3>100% literal-support overlap</h3><p>REGISTRY-MEASUREMENT: one hash-pinned prior covers every allowed location within three pixels when all positive pixels are treated as dots. This is not a score; the shared template's two-phase interpretation is noted above.</p></section>
<section><span>02</span><h3>No slots used</h3><p>No new experiment or competition upload was made in this turn.</p></section>
<section><span>03</span><h3>Fail-closed</h3><p>Shared pinned validator, no silent clipping, no dense-prior exemption, and no submission download when the uniqueness gate fails.</p></section></div>
<section><p class="eyebrow">WHY THE GATE STOPS</p><h2>A preflight proof, not a geological score.</h2>
<p>The pinned prior has positive support at every footprint pixel. Under the literal <code>finite &amp; value &gt; 0</code> support definition, every nonempty candidate dot set lies in its three-pixel halo. This is a sufficient rejection witness under that reading, not an interpretation-independent uniqueness theorem. The pinned template also provides a like-for-like continuous-surface reading; the prompt's intended semantics remain unresolved. We do not claim a complete registry scan.</p>
<p><a href="evidence/preflight.json">Read the independently recomputed proof ↗</a></p></section>
<section><p class="eyebrow">WHAT THE H33 RASTER DOES — AND DOES NOT — SHOW</p>
<h2>Efficient emission is a plausible explanation, not proven causality.</h2>
<p>The inspected reference contains 37,654 binary positive pixels, with median nearest-dot spacing of three pixels and no positive pixels on the mapped catalogue. These are REFERENCE-BYTE-MEASUREMENTS, not performance scores. Under the max-cover DTI, sparse placement can reduce redundant false-positive mass, while a mapped-fault collar can remove mass that adds little new-label coverage.</p>
<p>The supplied 0.2778 is USER-REPORTED; the pinned H33 build receipt says UNSCORED and no submission-page receipt ties that raster to a result. The prior dated public-board observation of 0.4413 is an OFFICIAL-LEADERBOARD-OBSERVATION, not this project's score. The prompt's 0.3195 may be stale. See the <a href="evidence/reference_audit.json">H33 byte audit</a> and <a href="research/review.md">scientific review</a>.</p></section>
<section><p class="eyebrow">NEXT GATES</p><h2>Evidence before promotion.</h2>
<ol><li>Resolve the shared literal-overlap contradiction and assign one method lane.</li><li>Restore organizer-authenticated cached features and verify provenance and licensing.</li><li>Run buffered whole-segment hide-and-recover using the pinned shared evaluator; rebuild catalogue features from visible faults only.</li><li>Test every feature alone on holdout; report pooled HOLDOUT-DTI, withheld positives, evaluator version, and a spatial-block-bootstrap 95% CI against a same-fold incumbent.</li><li>Audit surface and final-dot uniqueness, write/read-back with the shared writer, then request separate selector approval.</li></ol></section>"""
    source_table = (
        '<section id="sources"><p class="eyebrow">SOURCE AUDIT · 21 OCTOBER 2026</p>'
        '<h2>What was checked—and what was not.</h2>'
        '<div class="table-wrap"><table><thead><tr><th>Source</th><th>Access / verification</th>'
        '<th>Claim supported</th></tr></thead><tbody>'
        + rows
        + '</tbody></table></div><p>Additional geothermal, ASTER, 3DEP, Landsat, and Sentinel-1 '
        'source leads have access notes and unverified AOI coverage in the '
        '<a href="research/external-source-screen.md">external-source screen</a>. '
        'This dated table is not an automatically refreshed feed.</p></section>'
    )

    summary = """<p class="eyebrow">EXECUTIVE SUMMARY / SUBMISSION GUIDE</p>
<h1>Is this ready to submit?<br>Not in this release.</h1>
<section class="stop"><h2>Do not upload a file from this project yet.</h2>
<p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: NO FILE.</strong>
<strong>OK TO SUBMIT: NO.</strong> No new candidate TIF is authorized. A prior-session candidate has been withdrawn after its final dots triggered the literal overlap gate, despite passing local format/range checks. The pinned template's like-for-like continuous-surface reading makes the interpretation ambiguous; no uniqueness clearance exists. The JSON decision card is audit evidence, not a competition submission.</p>
<a class="button" href="evidence/run-card.json" download>Download decision card ↓</a></section>
<section><h2>What a future ready artifact must pass</h2><ul>
<li>A genuinely new prediction, not a renamed historical raster.</li>
<li>A single-band float32 GeoTIFF matching the sample CRS, shape and geotransform; finite values in [0,1] inside the footprint and an explicit outside-footprint policy.</li>
<li>Feature-by-feature leakage canaries on spatially withheld segments; any AUC above 0.90 is a leakage stop until explained.</li>
<li>Buffered whole-segment hide-and-recover, visible-only catalogue features, pixel-exact masking, pinned pooled HOLDOUT-DTI, withheld-positive count, evaluator version, and a spatial-block-bootstrap 95% CI that beats a compatible same-fold incumbent.</li>
<li>Pre-placement surface and final-dot registry checks; shared-writer read-back receipt; SHA256; unique name and note no longer than 140 characters.</li>
<li>Separate selector approval before any weekly submission slot is used.</li></ul></section>
<section><h2>Exact organizer upload steps, after every gate passes</h2><ol>
<li>Download only the prominent TIF explicitly authorized by a future run card and selector. This release has no submission file.</li>
<li>Open the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">competition</a>, sign in, review the official rules and your remaining allowance, then open “New submission”. This project has no authenticated competition access.</li>
<li>For “File to submit”, choose the approved single-band GeoTIFF, or a ZIP containing exactly one GeoTIFF.</li>
<li>Copy the approved short note from that artifact's writer receipt.</li>
<li>Submit only after selector approval. Save the organizer's receipt and score against the exact artifact SHA256.</li></ol>
<p>These are future instructions, not an instruction to upload now. A local validator cannot guarantee organizer acceptance or scientific usefulness.</p></section>
<section><h2>About “Predicted values must be in range [0, 1]”</h2>
<p>The rejected file was not supplied, so its cause cannot be diagnosed. NaN, infinity, nodata sentinels, or an out-of-range model output are possible causes, not findings. The shared local validator checks finite values and range before promotion; it never silently clips. The inherited ASB raster passes this local check, but fails uniqueness and does not explain the separate rejection.</p></section>
<section><h2>Research and limitations</h2><p>H33's reported 0.2778 is USER-REPORTED, not ORGANIZER-CONFIRMED; its pinned build receipt says UNSCORED. The answer and four ranked, conditional hypotheses are in the <a href="research/review.md">scientific review</a>. The full feature stack, organizer-authenticated data access, current holdout result, live leaderboard feed, submission-page allowance, and organizer acceptance are not available in this release.</p></section>"""

    legacy_page = f"""<p class="eyebrow">ARCHIVED NEGATIVE RESULT</p>
<h1>NOT A SUBMISSION — DO NOT DOWNLOAD OR SUBMIT.</h1>
<section class="stop"><h2>The inherited ASB raster is withdrawn from current downloads.</h2>
<p>Its local format checks passed. Under the literal positive-pixel support definition, exact final-dot overlap against the pinned dense registry witness is <strong>100% (REGISTRY-MEASUREMENT)</strong>, above the 70% threshold. The pinned template also classifies this witness as a continuous surface and says that overlap is not dot-field duplicate evidence; the user protocol does not resolve this. The file is no longer present in this Pages tree; its recorded SHA256 is <code>{html.escape(card['raster_sha256'])}</code>.</p>
<p>The pre-emission surface was not retained. The prior HOLDOUT-DTI receipt used local/private v81.1 code and a two-draw range, not a valid 95% CI from the pinned shared evaluator; it is not promotion evidence.</p>
<p><a href="evidence/legacy-candidate-audit.json">Read the format and registry audit JSON</a> · <a href="evidence/run-card.json">Read the canonical negative run card</a></p>
<p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: NO FILE. OK TO SUBMIT: NO.</strong></p></section>"""

    (DOCS / "index.html").write_text(header + home + source_table + footer)
    (DOCS / "executive-summary.html").write_text(header + summary + footer)
    (DOCS / "asb-candidate.html").write_text(header + legacy_page + footer)
    (DOCS / ".nojekyll").write_text("")
    print("Published fail-closed status site; no submission TIFF or link is available.")


if __name__ == "__main__":
    main()
