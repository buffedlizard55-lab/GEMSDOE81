"""The private unbuffered evaluator is retired; use the pinned shared tools.

Original code remains in Git at a53c822 for auditing the legacy measurements.
There is intentionally no drop-in make_draws replacement: silently substituting
fold definitions would make historical results and new validation incomparable.
"""


def _retired(*args, **kwargs):
    raise RuntimeError(
        'Private gems81 holdout retired: use vendor/gems57/evaluate_holdout.py '
        'with buffered segment folds, fold-visible catalogue features and spatial CI.'
    )


make_draws = evaluate = auc_score = _retired
