# Data placement

No competition data are present in this checkout. Download the authorized competition files only through the official [DrivenData data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) after signing in and enrolling. Do not bypass authentication, commit credentials, or place private data in the repository.

The official problem page names `training_features.tif` and the competition data page provides labels and the sample submission. This repository currently has no download/prepare/train/inference scripts, no template pin, and no cached feature stack; data placement alone will **not** make this checkout's training pipeline ready. Use the shared template and its documented data manifest/evaluator/writer in a future authorized lane.

Recommended local-only locations for eventual raw/processed data are `data/raw/` and `data/processed/`; these paths are ignored by Git. Before using any additional source, record its official URL, licence, geographic coverage, file hash, and sponsor-sharing permission.
