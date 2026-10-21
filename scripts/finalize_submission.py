#!/usr/bin/env python3
"""Retired finalizer for the noncompliant legacy ASB experiment.

This used to execute file writes at import time and relied on a private writer.
It is now safe to import and deliberately creates no submission artifact.
"""
from __future__ import annotations

if __package__:
    from .build_submission import main
else:  # Direct script execution has no package context.
    from build_submission import main


if __name__ == "__main__":
    raise SystemExit(main())
