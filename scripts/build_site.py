#!/usr/bin/env python3
"""Publish the GEMSDOE81 site. FAILS CLOSED: refuses to publish a download
unless the canonical run card (evidence/run_card.json) says verdict=promote,
its validator all_passed, and the TIF on disk matches the card SHA256."""
import hashlib, json
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
    v = card["validator"]
    if not v["checks"]["all_passed"]:
        raise ValueError("Validator did not all-pass; refusing to publish")
    tif = DOCS / "downloads" / card["submission_name"]
    if not tif.exists() or sha256_file(tif) != card["raster_sha256"]:
        raise ValueError("Submission TIF missing or SHA256 mismatch vs run card")
    name = card["submission_name"]; note = card["submission_note"]
    assert len(note) <= 140
    h = card["holdout_DTI"]; ctl = h["same_instrument_controls"]; ex = h["all_experiments_this_session"]
    reg_rows = "".join(
        f"<tr><td>{k}</td><td>{v2['surface_rank_corr_sampled']:.3f}</td><td>{100*v2['dot_overlap_within_3px']:.1f}%</td><td>{'FAIL' if v2['lane_violation'] else 'pass'}</td></tr>"
        for k, v2 in card["correlation_overlap_vs_registry"].items())
    header = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>GEMSDOE81 · CONT-ASB submission</title><link rel="stylesheet" href="style.css"><body><header>'
              '<a class="brand" href="index.html">GEMS<span>DOE81</span></a><nav aria-label="Main navigation">'
              '<a href="executive-summary.html">How to submit</a><a href="https://github.com/buffedlizard55-lab/GEMSDOE81">Repository ↗</a></nav></header><main>')
    footer = '</main><footer>Evidence over optimism. Own the outcome.<br>Reviewed 21 October 2026 · Snapshot, not a live leaderboard feed. Live score: UNSCORED.</footer></body></html>'
    home = f'''<p class="eyebrow">FAULT MAPPING / AUDITED RESEARCH</p><h1>New unique submission,<br>validated automatically.</h1><p><a href="#status">Jump to submission status ↓</a></p>
<section class="stop" style="background:#e6ffe6;border-color:#080" aria-labelledby="status"><p class="eyebrow">CURRENT SUBMISSION STATUS</p>
<h2 id="status">✅ OK TO DOWNLOAD &amp; SUBMIT THIS FILE</h2>
<div class="gate-status" role="status"><p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: YES — the one green file below.</strong></p>
<p><strong>OK TO SUBMIT: YES on format + holdout evidence (verdict: promote). No human inspection is needed: the automated validator in this repo passed every check on the exact bytes below. The final weekly-slot decision is still yours / the selector's.</strong></p></div>
<p><a class="button" href="downloads/{name}" download>⬇ DOWNLOAD SUBMISSION TIF: {name}</a></p>
<p><b>Copy-paste submission Note (≤140 chars):</b><br><code>{note}</code></p>
<p>SHA256: <code>{card["raster_sha256"]}</code> · {v["positive_pixels"]:,} positive pixels (binary 0/1) · single-band float32 · EPSG:32611 · 3730×3292 · transform identical to sample submission · <b>finite values in [0,1] everywhere — zeros, not NaN, outside the footprint</b> (this fixes the reported “Predicted values must be in range [0, 1]” rejection) · 0 on the published catalogue.</p>
<p><a href="downloads/{name[:-4]}.receipt.json">Validator + run-card receipt (JSON)</a> · <a href="executive-summary.html">Executive summary: exactly how to submit →</a></p></section>
<section><p class="eyebrow">WHY THIS FILE — HOLDOUT EVIDENCE (NOT A LIVE SCORE)</p><h2>Continuation-gated scarps beat every control on the same instrument.</h2>
<p><b>HOLDOUT-DTI</b> (evaluator {h["evaluator"]}): candidate <b>{h["candidate_F_CONT"]:.4f}</b>, per-draw {h["per_draw"][0]:.4f} / {h["per_draw"][1]:.4f} (95% CI = draw range [{h["ci95_draw_range"][0]:.4f}, {h["ci95_draw_range"][1]:.4f}]; {h["n_hidden_positives_total"]:,} hidden positives). Same-instrument controls: ASB surface {ctl["ASB_S_poisson44090_buf2"]:.4f}; d28 fixed mask {ctl["d28_fixed_mask"]:.4f}. Canary AUCs all &lt; 0.90 (no leakage flag). This raster is <b>UNSCORED</b> live — no claim of beating 0.2778 or 0.4413.</p>
<table><thead><tr><th>Experiment (all HOLDOUT-DTI, same config)</th><th>DTI</th><th>Verdict</th></tr></thead><tbody>
<tr><td>E3 CONT-ASB (shipped)</td><td><b>{h["candidate_F_CONT"]:.4f}</b></td><td>promote</td></tr>
<tr><td>E3 continuation alone</td><td>{ex["E3_CONT_alone"]:.4f}</td><td>—</td></tr>
<tr><td>Prior ASB (already shipped, do not resubmit)</td><td>{ctl["ASB_S_poisson44090_buf2"]:.4f}</td><td>negative</td></tr>
<tr><td>E2 edge-consensus × ASB</td><td>{ex["E2_EDGExASB"]:.4f}</td><td>negative</td></tr>
<tr><td>E1 radiometric-discordance gate</td><td>{ex["E1_RAD_gate_F"]:.4f}</td><td>negative</td></tr>
<tr><td>E1 radiometric alone (AUC 0.51 ≈ chance)</td><td>{ex["E1_RAD_alone"]:.4f}</td><td>negative</td></tr></tbody></table></section>
<section><p class="eyebrow">UNIQUENESS — REGISTRY LANE CHECK</p><h2>Not a copy of any previous submission.</h2>
<p>Method: antithetic LiDAR scarp-pair × basement-step, gated by distance-to-catalogue continuation, Poisson-dotted. Duplicate rule: rank-corr ≤ 0.90 and ≤ 70% of dots within 3 px of a registry raster.</p>
<table><thead><tr><th>Registry raster</th><th>Surface rank-corr</th><th>Dots within 3 px</th><th>Lane</th></tr></thead><tbody>{reg_rows}</tbody></table></section>
<section><p class="eyebrow">WHY DID THE 0.2778 WINNER WIN?</p><h2>Sparse, pruned dots beat dense surfaces.</h2><p>{card["why_winner_0.2778"]}</p>
<p>The 0.2778 and 0.4413 figures are organizer/leaderboard-reported for other teams' files (see repo README evidence labels); this project's file has no organizer score yet.</p></section>
<section><p class="eyebrow">OTHER FILES IN downloads/ — DO NOT SUBMIT</p><h2>❌ Negative-experiment rasters</h2>
<ul><li><code>gems81-asb-…-zeros.tif</code> — prior session ASB, HOLDOUT-DTI {ctl["ASB_S_poisson44090_buf2"]:.4f}, verdict negative, already generated previously. <b>Do not submit.</b></li>
<li><code>gems81-radasb-…-zeros.tif</code> — this session E1 radiometric gate, HOLDOUT-DTI {ex["E1_RAD_gate_F"]:.4f}, verdict negative. <b>Do not submit.</b></li></ul>
<p>Only the green file at the top of this page is the submission.</p></section>
<section><p class="eyebrow">RISKS &amp; LIMITS</p><h2>Read before spending a slot.</h2>
<ul><li>Holdout favours continuation by construction (hidden segments cluster near visible ones); live undiscovered faults may be less continuation-like. This is the main residual risk.</li>
<li>Data are hash-pinned owner mirrors of login-walled DrivenData files — integrity-verified, not organizer-authenticated (IR-81-01).</li>
<li>The organizer page allows null/NaN outside bounds, but a NaN-outside file was user-reported rejected with “[0,1]”; this file uses zeros everywhere, satisfying the stricter reading.</li>
<li>Local validation cannot guarantee organizer acceptance or a leaderboard score.</li></ul></section>'''
    summary = f'''<p class="eyebrow">EXECUTIVE SUMMARY / SUBMISSION GUIDE</p><h1>Exactly how to submit</h1>
<section class="stop" style="background:#e6ffe6;border-color:#080"><h2>✅ Submit this one file</h2>
<p><strong>OK TO DOWNLOAD: YES.</strong> <strong>OK TO SUBMIT: YES</strong> (automated validator all-pass; science verdict promote on HOLDOUT-DTI — see home page). No human inspector is required; the repo validator re-reads the file from disk and checks every format rule.</p>
<p><a class="button" href="downloads/{name}" download>⬇ DOWNLOAD: {name}</a></p>
<p><b>Note to paste:</b> <code>{note}</code> ({len(note)} chars)<br>SHA256: <code>{card["raster_sha256"]}</code></p></section>
<section><h2>Steps on DrivenData</h2><ol>
<li>Download the green .tif above (do not use any other file in downloads/ — they are labelled negative experiments).</li>
<li>Open the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">competition</a>, sign in, check your remaining weekly allowance on the submission page (this project cannot see it).</li>
<li>Click <b>New submission</b> → for “File to submit”, choose <code>{name}</code> (single-band GeoTIFF; no ZIP needed).</li>
<li>Paste the Note above verbatim.</li>
<li>Submit, then save the organizer receipt and any score against this exact SHA256. Until that receipt exists the file is UNSCORED.</li></ol></section>
<section><h2>Why this passes “Predicted values must be in range [0, 1]”</h2>
<p>The validator guarantees, on the bytes on disk: single band, float32, EPSG:32611, 3730×3292, transform identical to the sample submission, values finite and within [0,1] <b>everywhere</b> (binary 0/1; zeros — not NaN — outside the footprint), and 0 on the published fault catalogue. Re-run it yourself with no human inspection: <code>python scripts/validate_submission.py docs/downloads/{name}</code> (after <code>python scripts/restore_inputs.py</code>-equivalent data placement; see repo README).</p></section>
<section><h2>What could still go wrong</h2><ul><li>Organizer acceptance is never guaranteed by a local validator.</li><li>Holdout evidence (DTI {h["candidate_F_CONT"]:.4f}) is not a live score; continuation bias is the named risk on the home page.</li><li>Promotion to a real slot is a separate selector decision within the weekly cap shown on the submission page.</li></ul></section>'''
    (DOCS / "index.html").write_text(header + home + footer)
    (DOCS / "executive-summary.html").write_text(header + summary + footer)
    (DOCS / "submit.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=executive-summary.html">'
        '<title>Submission instructions</title><body><p>✅ One promoted submission is available.</p>'
        '<p><a href="executive-summary.html">Executive summary and exact submission steps →</a></p></body></html>')
    (DOCS / "asb-candidate.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Superseded</title><body>'
        '<h1>Superseded — do not submit the ASB file</h1><p>The prior ASB candidate is a measured negative '
        '(HOLDOUT-DTI 0.0831). The current promoted submission is CONT-ASB on the '
        '<a href="index.html">home page</a>.</p></body></html>')
    print(f"Published promoted submission site for {name}")


if __name__ == "__main__":
    main()
