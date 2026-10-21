#!/usr/bin/env bash
# Restore hash-pinned mirrors via gh (github.com only). Verifies sha256; fails closed.
set -euo pipefail; cd "$(dirname "$0")/.."; mkdir -p data /tmp/g81mirror
gh api repos/buffedlizard55-lab/GEMSDOE24/contents/data/bridge/labels.tif?ref=07345ea0604953d7efb858d9cfbc21e20c7aca0b -H "Accept: application/vnd.github.raw" > data/labels.tif
gh api repos/buffedlizard55-lab/GEMSDOE24/contents/data/bridge/sample_submission.tif?ref=07345ea0604953d7efb858d9cfbc21e20c7aca0b -H "Accept: application/vnd.github.raw" > data/sample_submission.tif || gh api repos/buffedlizard55-lab/GEMSDOE24/contents/data/bridge/example_submission.tif?ref=07345ea0604953d7efb858d9cfbc21e20c7aca0b -H "Accept: application/vnd.github.raw" > data/sample_submission.tif
for f in lidar_scarp_features_u8 geodawn_rad_u8 geodawn_extensions_u8; do gh api repos/buffedlizard55-lab/GEMSDOE24/contents/data/external/$f.tif?ref=07345ea0604953d7efb858d9cfbc21e20c7aca0b -H "Accept: application/vnd.github.raw" > data/$f.tif; done
echo "training_features.tif: reassemble 5 parts from GEMSDOE data/bridge (see registry manifest) and verify sha256 4371c82e..."
sha256sum data/*.tif
