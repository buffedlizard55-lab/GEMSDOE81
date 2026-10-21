#!/usr/bin/env python3
"""Retired unsafe private-evaluator runner. No candidate construction permitted.

Historical implementation is in Git at a53c822. Replaced because it bypassed the
binding registry witness, relied on /tmp state and mislabelled CI/performance.
"""
from blocked_generation import main

if __name__ == '__main__':
    raise SystemExit(main())
