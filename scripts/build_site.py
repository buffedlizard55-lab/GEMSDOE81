#!/usr/bin/env python3
"""Publish one authoritative negative decision and an explicitly research-only TIFF."""
import html
import json
import shutil
from pathlib import Path

from audit import sha256

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'


def main():
    card = json.loads((ROOT/'evidence/run-card.json').read_text())
    proof = json.loads((ROOT/'evidence/preflight.json').read_text())
    if (card['authorized_to_download_and_submit'] is not False or card['verdict'] != 'negative'
            or card['registry']['decision'] != 'duplicate'
            or proof.get('decision') != 'STOP_UNIVERSAL_DUPLICATE'
            or proof.get('authorized_to_submit') is not False):
        raise ValueError('Blocked-release publisher cannot publish candidate authorization')
    name = card['submission_name']
    if Path(name).name != name or not name.endswith('.tif'):
        raise ValueError('invalid artifact name')
    if sha256(DOCS/'downloads'/name) != card['raster_sha256']:
        raise ValueError('negative artifact hash mismatch; re-audit before publishing')
    out = DOCS/'evidence'
    out.mkdir(parents=True, exist_ok=True)
    for filename in ['preflight.json', 'run-card.json', 'reference_audit.json', 'legacy-asb.json']:
        shutil.copyfile(ROOT/'evidence'/filename, out/filename)
    sources = json.loads((ROOT/'registry/sources.json').read_text())
    esc = html.escape
    rows = ''.join(f'<tr><td><a href="{esc(s["url"], quote=True)}">{esc(s["name"])}</a></td><td>{esc(s["status"])}</td><td>{esc(s["supports"])}</td></tr>' for s in sources['sources'])
    header = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GEMSDOE81 · Submission audit</title><link rel="stylesheet" href="style.css"><body><header><a class="brand" href="index.html">GEMS<span>DOE81</span></a><nav aria-label="Main navigation"><a href="executive-summary.html">How to submit</a><a href="research/review.md">Research</a><a href="https://github.com/buffedlizard55-lab/GEMSDOE81">Repository ↗</a></nav></header><main>'''
    footer = '''</main><footer>Evidence over optimism. Own the outcome.<br>Reviewed 21 October 2026 · Snapshot, not a live leaderboard feed.</footer></body></html>'''
    gate = '''<section class="stop"><p class="eyebrow">CURRENT SUBMISSION STATUS</p><h2>DO NOT SUBMIT — duplicate / negative research artifact.</h2><p><strong>OK TO DOWNLOAD AS A COMPETITION SUBMISSION: NO APPROVED FILE.</strong></p><p><strong>OK TO SUBMIT: NO.</strong> Local format validation passed, but the binding registry check rejects the inherited candidate. A separate selector has not authorized a weekly slot.</p><button disabled>Approved submission TIF unavailable</button><p><a href="evidence/run-card.json" download>Download authoritative negative run card ↓</a></p></section>'''
    download = f'''<section><p class="eyebrow">RESEARCH DOWNLOAD ONLY · NOT A COMPETITION SUBMISSION</p><h2>Existing TIFF, independently rechecked.</h2><p>The inherited ASB artifact remains available for reproducibility. It is not a submission file approved by this project. No new TIFF was generated during this review.</p><p><a class="button" href="downloads/{esc(name, quote=True)}" download>Download negative research TIFF — DO NOT SUBMIT ↓</a></p><p><code>{esc(name)}</code></p><p>SHA256: <code>{esc(card['raster_sha256'])}</code></p><p>Research note (not an upload instruction): <code>{esc(card['note'])}</code></p><p>The shared validator confirms one float32 band, matching CRS/shape/transform, no NaN or infinity, values in [0,1] everywhere, and zero on catalogue/outside footprint. Registry overlap is 100% against a verified dense prior, exceeding the 70% limit. This is a registry measurement, not a performance score.</p><p><a href="evidence/run-card.json">Shared-validator output + decision</a> · <a href="evidence/preflight.json">Candidate-independent proof</a></p></section>'''
    home = '''<p class="eyebrow">FAULT MAPPING / AUDITED RESEARCH</p><h1>A valid file is not<br>a validated discovery.</h1><p class="lead">Automated checks distinguish local format validity, registry uniqueness, scientific validation, and permission to submit.</p><p><a href="#sources">Jump to source audit ↓</a> · <a href="executive-summary.html">Executive summary / exact submission steps →</a></p>'''+gate+download+'''
<div class="metrics"><section><span>01</span><h3>Format pass</h3><p>Inherited TIFF passes pinned shared read-back checks. This does not guarantee organizer acceptance.</p></section><section><span>02</span><h3>Uniqueness fail</h3><p>100% dot overlap with a dense registered prior. Original surface was not preserved; the universal proof also rejects nonempty in-footprint surface support.</p></section><section><span>03</span><h3>No slots used</h3><p>No new candidate, geological experiment, holdout, or competition upload in this review.</p></section></div>
<section><h2>Why H33 might have worked</h2><p>The reference byte audit shows 37,654 binary dots, median nearest-dot spacing three pixels, and no positives on the catalogue. Efficient thinning and catalogue-collar pruning plausibly reduce redundant prediction mass. Hidden labels are required to establish causation or superiority.</p><p><strong>0.2778 is USER-REPORTED, not ORGANIZER-CONFIRMED.</strong> No artifact-linked organizer receipt is available. The inherited public-leaderboard observation of 0.4413 is a dated snapshot, not this project’s score or a fresh leaderboard check.</p><p><a href="evidence/reference_audit.json">Reference byte audit</a> · <a href="research/review.md">Scientific review and four ranked hypotheses</a></p></section>
<section><h2>Corrections from this review</h2><ul><li>Removed the conflicting “OK to submit” candidate-page message.</li><li>Retracted a two-draw range incorrectly labelled as a 95% CI.</li><li>Retired private-evaluator runners and a writer that silently converted invalid floats to binary dots.</li><li>Preserved legacy measurements as unaccepted historical records, not scientific validation.</li></ul><p><a href="research/session-review.md">Three-pass review, limitations and next steps</a> · <a href="evidence/legacy-asb.json">Legacy measurement audit</a></p></section>
<section><h2>Before another experiment</h2><ol><li>Resolve the shared dense-prior protocol contradiction and assign one unique lane.</li><li>Verify shared cached inputs; use buffered whole-segment hide-and-recover with fold-visible catalogue features only.</li><li>Test every raw feature on withheld positives; compute pooled HOLDOUT-DTI and spatial 95% CI with the shared evaluator against a same-fold incumbent.</li><li>Pass surface and final-dot registry gates, shared writer read-back, then separate selector approval. Never infer a leaderboard score from a projection.</li></ol></section>'''
    source_table = '<section id="sources"><p class="eyebrow">DATED SOURCE AUDIT</p><h2>Evidence and access limits.</h2><p>'+esc(sources['freshness_note'])+'</p><div class="table-wrap"><table><thead><tr><th>Source</th><th>Access / verification</th><th>Claim supported</th></tr></thead><tbody>'+rows+'</tbody></table></div><p>Additional leads and unverified target-area coverage: <a href="research/external-source-screen.md">external-source screen</a>. These are not claims of obtainable new data here.</p></section>'
    summary = '''<p class="eyebrow">EXECUTIVE SUMMARY / SUBMISSION GUIDE</p><h1>Download exists.<br>Submission is blocked.</h1>'''+gate+download+'''
<section><h2>Exactly how submission will work after approval</h2><ol><li>Download the future <strong>approved new .tif</strong>, not this negative research artifact, a JSON card, HTML page or historical baseline.</li><li>Sign in at the <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">official competition</a>, review rules and authenticated remaining allowance, then open New submission. No slot is used by local validation.</li><li>Under “File to submit”, choose the single-band TIFF or ZIP containing exactly one TIFF, matching the template CRS, shape and geotransform.</li><li>Copy the approved distinguishing note of at most 140 characters from its writer receipt.</li><li>Submit only after separate selector approval. Retain the organizer receipt and score against the artifact SHA256. None exists for this artifact.</li></ol><p>These are future instructions, not authorization to upload now. The authenticated weekly allowance is unknown.</p></section>
<section><h2>Local automated checks versus scientific validation</h2><p>The inherited file passes local shared format checks without human inspection. It fails the literal registry gate. No accepted HOLDOUT-DTI or spatial 95% CI is available. Legacy private-evaluator measurements are preserved but rejected as promotion evidence: they used no prescribed segment buffer, a two-draw range rather than a CI, and a full-catalogue AUC rather than a withheld-positive canary.</p></section>
<section><h2>About “Predicted values must be in range [0, 1]”</h2><p>The failed file was not supplied; the cause remains unknown. NaN, infinity, out-of-range predictions or nodata sentinels are possible causes, not diagnoses. The shared writer rejects invalid predictions before serialization and validates the on-disk result. Zeros outside the footprint are a conservative local policy, not proof of organizer acceptance. Never silently clip or coerce model errors.</p></section>
<section><h2>Limitations and next work</h2><p>New experiment blocked by the registry rule and absent lane assignment. Cached feature stack not restored; no organizer-authenticated data, artifact-linked score receipt, or weekly-cap access. The official reference README supports CPU-only operation; GPU is faster, not mandatory. Outbound access here is limited to GitHub and package registries, so no fresh official leaderboard, USGS payload or rules PDF check is claimed.</p><p><a href="research/session-review.md">Review and exact next-session gates</a></p></section>'''
    candidate = '<p class="eyebrow">SUPERSEDES PRIOR CONFLICTING CANDIDATE PAGE</p><h1>ASB is a negative<br>research artifact.</h1>'+gate+download+'<p>The earlier approval and organizer-confirmation claims were unsupported and have been withdrawn. <a href="research/session-review.md">Read the corrective audit</a>.</p>'
    for filename, content in [('index.html', home+source_table), ('executive-summary.html', summary), ('asb-candidate.html', candidate)]:
        (DOCS/filename).write_text(header+content+footer)
    (DOCS/'.nojekyll').write_text('')
    print('Published one negative decision with research-only TIFF download; no submission authorization.')


if __name__ == '__main__':
    main()
