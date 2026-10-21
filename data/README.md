# Data placement and provenance

This checkout does **not** contain an organizer-authenticated training stack or the full cached feature set. The competition data page is login-gated; use it only through an authorized account and do not bypass authentication, commit credentials, or place private data in Git.

For the documented duplicate preflight only, `scripts/restore_inputs.py` restores three SHA-pinned audit inputs from owner-supplied GitHub mirrors: the sample grid, the existing-fault catalogue, and one dense registry witness. They are placed under ignored `data/bridge/` and `.cache/registry/` paths. Matching hashes establish mirror integrity—not organizer origin, licensing, permission to train, or competition acceptance. The restored witness is sufficient for the recorded negative decision; it is not a full feature stack.

The shared `gems57` evaluator, writer, and related code are pinned by `registry/template_pin.json` and live under `vendor/gems57/`. Do not create a private fork or interpret their presence as authorization to generate a candidate. The earlier `scripts/download_competition_data.sh` and `scripts/prepare_data.py` commands do not exist in this checkout; data placement alone does not make a training pipeline ready.

Before any future use of external data, verify the official source, license, geographic coverage, bytes and hash, temporal coverage, and permission to use or redistribute it. Keep raw and processed data out of Git under ignored paths.
