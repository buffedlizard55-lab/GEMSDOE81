#!/usr/bin/env python3
"""Restore only rejection-proof inputs, from hash-pinned owner mirrors, not official data authentication."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def restore(repo, ref, path, expected, dest):
    dest = ROOT / dest
    if dest.exists():
        with dest.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() == expected:
                return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix('.partial')
    try:
        with tmp.open('wb') as out:
            subprocess.run(['gh','api',f'repos/{repo}/contents/{path}?ref={ref}',
                            '-H','Accept: application/vnd.github.raw'], stdout=out, check=True)
        with tmp.open('rb') as f:
            if hashlib.file_digest(f,'sha256').hexdigest() != expected:
                raise ValueError(f'hash mismatch: {path}')
        tmp.replace(dest)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    manifest = json.loads((ROOT/'registry/data_manifest.json').read_text())
    for e in manifest['files']:
        if e['id'] in ('sample_submission','existing_faults'):
            restore(e['repo'], e['ref'], e['path'], e['sha256'], 'data/bridge/'+e['dest'])
    e = json.loads((ROOT/'registry/witness_sources.json').read_text())['dense_witness']
    restore(e['repo'], e['ref'], e['path'], e['sha256'], '.cache/registry/dense_witness.tif')
    print('Verified rejection-proof inputs. No training feature stack or official authentication claimed.')


if __name__ == '__main__':
    main()
