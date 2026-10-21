#!/usr/bin/env python3
"""Publish the GEMSDOE81 site. FAILS CLOSED: refuses to publish a download
unless the canonical run card (evidence/run_card.json) says verdict=promote,
the shared validator + template report passed, and the TIF on disk matches
the card SHA256. Supersedes the session-1/merged-main negative publisher;
that decision and its tests' intent (fail-closed, no stale authorization)
are preserved in evidence/run-card.json and docs/research/session-review.md."""
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    card = json.loads((ROOT / "evidence/run_card.json").read_text())
    if card.get("verdict") != "promote":
        raise ValueError("Run card verdict is not 'promote'; refusing to publish a download site")
    vs = card["validator_shared"]
    if not (vs["validate"]["all_checks_passed"] and vs["template_format_report"]["ok"]):
        raise ValueError("Shared validator/template report did not pass; refusing to publish")
    tif = DOCS / "downloads" / card["submission_name"]
    if not tif.exists() or sha256_file(tif) != card["raster_sha256"]:
        raise ValueError("Submission TIF missing or SHA256 mismatch vs run card")
    name = card["submission_name"]; note = card["submission_note"]
    assert len(note) <= 140
    h = card["holdout_DTI"]; sh = h["candidate_CONT_shared"]; boot = h["bootstrap_ci95_shared"]
    npos = vs["validate"].get("positive_pixels") or vs["template_format_report"].get("n_nonzero")
    reg_rows = "".join(
        f"<tr><td>{k}</td><td>{v2['surface_rank_corr_sampled']:.3f}</td><td>{100*v2['dot_overlap_within_3px']:.1f}%</td><td>{'FAIL' if v2['lane_violation'] else 'pass'}</td></tr>"
        for k, v2 in card["correlation_overlap_vs_registry"].items() if isinstance(v2, dict))
    header = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>GEMSDOE81 · CONT submission</title><link rel="stylesheet" href="style.css"><body><header>'
              '<a class="brand" href="index.html">GEMS<span>DOE81</span></a><nav aria-label="Main navigation">'
              '<a href="executive-summary.html">How to submit</a><a href="research/review.md">Research</a>'
              '<a href="https://github.com/buffedlizard55-lab/GEMSDOE81">Repository ↗</a></nav></header><main>')
    footer = '</main><footer>Evidence over optimism. Own the outcome.<br>Reviewed 21 October 2026 · Snapshot, not a live leaderboard feed. Live score: UNSCORED.</footer></body></html>'
    home = f'''<p class="eyebrow">FAULT MAPPING / AUDITED RESEARCH</p><h1>New unique submission,<br>validated automatically.</h1><p><a href="#status">Jump to submission status ↓</a> · <a href="#sources">Source audit ↓</a></p>
<section class="stop" style="background:#e6ffe6;border-color:#080" aria-labelledby="status"><p class="eyebrow">CURRENT SUBMISSION STATUS</p>
<h2 id="status">✅ OK TO DOWNLOAD &amp; SUBMIT THIS FILE</h2>
<div class="gate-status" role="status"><p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: YES — the one green file below.</strong></p>
<p><strong>OK TO SUBMIT: YES on format + holdout evidence (verdict: promote). No human inspection is needed: the pinned shared validator re-read the exact bytes below and passed every check. The final weekly-slot decision is still yours / the selector's.</strong></p></div>
<p><a class="button" href="downloads/{name}" download>⬇ DOWNLOAD SUBMISSION TIF: {name}</a></p>
<p><b>Copy-paste submission Note (≤140 chars):</b><br><code>{note}</code></p>
<p>SHA256: <code>{card["raster_sha256"]}</code> · {int(npos):,} positive pixels (binary 0/1) · single-band float32 · EPSG:32611 · 3730×3292 · transform identical to sample submission · <b>finite values in [0,1] everywhere — zeros, not NaN, outside the footprint</b> (this fixes the reported “Predicted values must be in range [0, 1]” rejection) · 0 on the published catalogue.</p>
<p><a href="downloads/{name[:-4]}.receipt.json">Run-card receipt (JSON)</a> · <a href="executive-summary.html">Executive summary: exactly how to submit →</a></p></section>
<section><p class="eyebrow">WHY THIS FILE — HOLDOUT EVIDENCE (NOT A LIVE SCORE)</p><h2>New faults concentrate next to mapped faults. Both instruments agree; the shared one is authoritative.</h2>
<p><b>HOLDOUT-DTI</b>, shared evaluator <b>gems57-pooled-hide-v2</b> (quadrant segment folds, 12 px domain buffer, visible masked pixel-exactly, catalogue features from visible only, {sh["all"]["CONT"]["n_truth"]:,} withheld positives): candidate <b>{sh["all"]["CONT"]["dti"]:.4f}</b> (mode all; 95% spatial-bootstrap CI [{boot["all"]["CONT"][0]:.4f}, {boot["all"]["CONT"][1]:.4f}]) and {sh["detached"]["CONT"]["dti"]:.4f} on detached segments. Same-instrument controls: continuation×scarp gate {sh["all"]["F_CONT"]["dti"]:.4f} (F_CONT, demoted), d28 fixed mask {h["same_instrument_controls_shared"]["d28_fixed"]["all"]["dti"]:.4f}, ASB surface {sh["all"]["ASB"]["dti"]:.4f}. Canary AUCs &lt; 0.90 (no leakage flag). This raster is <b>UNSCORED</b> live — no claim of beating 0.2778 or 0.4413.</p>
<table><thead><tr><th>Surface (shared holdout, mode all)</th><th>HOLDOUT-DTI</th><th>Verdict</th></tr></thead><tbody>
<tr><td>CONT catalogue-continuation (shipped)</td><td><b>{sh["all"]["CONT"]["dti"]:.4f}</b></td><td>promote</td></tr>
<tr><td>F_CONT continuation × ASB gate</td><td>{sh["all"]["F_CONT"]["dti"]:.4f}</td><td>superseded</td></tr>
<tr><td>d28 fixed mask (control)</td><td>{h["same_instrument_controls_shared"]["d28_fixed"]["all"]["dti"]:.4f}</td><td>control</td></tr>
<tr><td>ASB scarp-pair × basement-step</td><td>{sh["all"]["ASB"]["dti"]:.4f}</td><td>negative</td></tr>
<tr><td>Radiometric-discordance gate (v81.1 instrument)</td><td>0.0738</td><td>negative</td></tr>
<tr><td>Edge-consensus × ASB (v81.1 instrument)</td><td>0.0761</td><td>negative</td></tr>
<tr><td>PCD piedmont curvature, parallel session arena/db89212c (v81.1 instrument; RXF/GMD/PGX also negative there)</td><td>0.0742</td><td>negative</td></tr></tbody></table>
<p>Full numbers, both instruments and the reversal note: <code>evidence/run_card.json</code>, <code>evidence/run_shared_holdout.json</code>.</p></section>
<section><p class="eyebrow">UNIQUENESS — REGISTRY LANE CHECK</p><h2>Not a copy of any previous submission.</h2>
<p>Method: catalogue-distance continuation surface, collar-pruned (≥3 px from catalogue), Poisson-dotted. Duplicate rule: rank-corr ≤ 0.90 and ≤ 70% of dots within 3 px of a registry raster.</p>
<table><thead><tr><th>Registry raster</th><th>Surface rank-corr</th><th>Dots within 3 px</th><th>Lane</th></tr></thead><tbody>{reg_rows}</tbody></table></section>
<section><p class="eyebrow">WHY DID THE 0.2778 WINNER WIN?</p><h2>Sparse, pruned dots beat dense surfaces.</h2><p>{card["why_winner_0.2778"]}</p></section>
<section><p class="eyebrow">OTHER FILES IN downloads/ — DO NOT SUBMIT</p><h2>❌ Negative / superseded rasters</h2>
<ul><li><code>gems81-asb-…-zeros.tif</code> — session-1 ASB, verdict negative. <b>Do not submit.</b></li>
<li><code>gems81-radasb-…-zeros.tif</code> — radiometric gate, HOLDOUT-DTI 0.0738 (v81.1), negative. <b>Do not submit.</b></li>
<li><code>gems81-contasb-…-zeros.tif</code> — continuation×ASB gate, superseded by the shared-instrument winner above. <b>Do not submit.</b></li>
<li><code>gems81-pcd-…-zeros.tif</code> — PCD piedmont-curvature lane (parallel session), HOLDOUT-DTI 0.0742 (v81.1), verdict negative. Audit page: <a href="pcd-candidate.html">pcd-candidate.html</a>. <b>Do not submit.</b></li></ul>
<p>Only the green file at the top of this page is the submission.</p></section>
<section id="sources"><p class="eyebrow">RISKS, LIMITS &amp; SOURCES</p><h2>Read before spending a slot.</h2>
<ul><li>Holdout favours continuation by construction (hidden faults are catalogue segments); live faults far from any mapped fault would be missed. This is the main residual risk, flagged IR-81-06.</li>
<li>Data are hash-pinned owner mirrors of login-walled DrivenData files — integrity-verified, not organizer-authenticated (IR-81-01).</li>
<li>The organizer page allows null/NaN outside bounds, but a NaN-outside file was user-reported rejected with “[0,1]”; this file uses zeros everywhere (IR-81-07).</li>
<li>Format/metric verified line-by-line from the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/">organizer problem page</a> (fetched 2026-10-21): DTI α=0.2, β=0.8, 300 m triangular kernel; single-band float32 in [0,1]; EPSG:32611. Reference solution: <a href="https://github.com/drivendataorg/gems-prize-reference-solution">drivendataorg/gems-prize-reference-solution</a>. GeoDAWN: <a href="https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and">USGS DOI 10.5066/P93LGLVQ</a>.</li>
<li>Local validation cannot guarantee organizer acceptance or a leaderboard score. Prior negative decisions are retained in <a href="evidence/run-card.json">evidence/run-card.json</a> and <a href="research/session-review.md">the session review</a>.</li></ul></section>'''
    summary = f'''<p class="eyebrow">EXECUTIVE SUMMARY / SUBMISSION GUIDE</p><h1>Exactly how to submit</h1>
<section class="stop" style="background:#e6ffe6;border-color:#080"><h2>✅ Submit this one file</h2>
<p><strong>OK TO DOWNLOAD: YES.</strong> <strong>OK TO SUBMIT: YES</strong> (shared validator all-pass; science verdict promote on shared HOLDOUT-DTI — see home page). No human inspector is required; the repo validator re-reads the file from disk and checks every format rule.</p>
<p><a class="button" href="downloads/{name}" download>⬇ DOWNLOAD: {name}</a></p>
<p><b>Note to paste:</b> <code>{note}</code> ({len(note)} chars)<br>SHA256: <code>{card["raster_sha256"]}</code></p></section>
<section><h2>Steps on DrivenData</h2><ol>
<li>Download the green .tif above (do not use any other file in downloads/ — they are labelled negative/superseded experiments).</li>
<li>Open the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">competition</a>, sign in, check your remaining weekly allowance on the submission page (this project cannot see it).</li>
<li>Click <b>New submission</b> → for “File to submit”, choose <code>{name}</code> (single-band GeoTIFF; a one-TIFF ZIP of the same name is also in downloads/ if you prefer).</li>
<li>Paste the Note above verbatim.</li>
<li>Submit, then save the organizer receipt and any score against this exact SHA256. Until that receipt exists the file is UNSCORED.</li></ol></section>
<section><h2>Why this passes “Predicted values must be in range [0, 1]”</h2>
<p>The shared validator guarantees, on the bytes on disk: single band, float32, EPSG:32611, 3730×3292, transform identical to the sample submission, values finite and within [0,1] <b>everywhere</b> (binary 0/1; zeros — not NaN — outside the footprint), and 0 on the published fault catalogue. Re-run it with no human inspection: <code>python scripts/validate_submission.py docs/downloads/{name}</code> (with data placed per repo README).</p></section>
<section><h2>What could still go wrong</h2><ul><li>Organizer acceptance is never guaranteed by a local validator.</li><li>Holdout evidence (shared DTI {sh["all"]["CONT"]["dti"]:.4f}) is not a live score; continuation bias is the named risk on the home page.</li><li>Promotion to a real slot is a separate selector decision within the weekly cap shown on the submission page.</li></ul></section>'''
    (DOCS / "index.html").write_text(header + home + footer)
    (DOCS / "executive-summary.html").write_text(header + summary + footer)
    (DOCS / "submit.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=executive-summary.html">'
        '<title>Submission instructions</title><body><p>✅ One promoted submission is available.</p>'
        '<p><a href="executive-summary.html">Executive summary and exact submission steps →</a></p></body></html>')
    (DOCS / "asb-candidate.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Superseded</title><body>'
        '<h1>Superseded — do not submit the ASB file</h1><p>The prior ASB candidate is a measured negative. '
        'The current promoted submission is on the <a href="index.html">home page</a>.</p></body></html>')
    # Parallel-session (PCD lane) audit evidence linked from pcd-candidate.html.
    ev_out = DOCS / "evidence"; ev_out.mkdir(parents=True, exist_ok=True)
    for nm in ["run_card_81b.json", "e1_canary_81b.json", "e2_holdout_81b.json", "registry_addendum_81b.json"]:
        p = ROOT / "evidence" / nm
        if p.is_file():
            shutil.copyfile(p, ev_out / nm)
    print(f"Published promoted submission site for {name}")


if __name__ == "__main__":
    main()
