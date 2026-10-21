#!/usr/bin/env python3
"""Dependency-free checks for the static GEMSDOE81 site and release-status card."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "executive-summary.html",
    "research.html",
    "sources.html",
    "irregularities.html",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()
        self.english_document = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang") == "en":
            self.english_document = True
        if tag == "a" and values.get("href"):
            self.hrefs.append(str(values["href"]))
        if values.get("id"):
            self.ids.add(str(values["id"]))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def check() -> list[str]:
    errors: list[str] = []
    page_parsers: dict[Path, PageParser] = {}

    for relative in PAGES:
        page = ROOT / relative
        if not page.is_file():
            errors.append(f"missing page: {relative}")
            continue
        parser = parse_page(page)
        page_parsers[page] = parser
        if not parser.english_document:
            errors.append(f"{relative}: missing <html lang=\"en\">")

    for page, parser in page_parsers.items():
        for href in parser.hrefs:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            target = (page.parent / parts.path).resolve() if parts.path else page
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: broken local link {href}")
                continue
            if parts.fragment and target.suffix.lower() in {".html", ".htm"}:
                target_parser = page_parsers.get(target)
                if target_parser is None:
                    if target.is_file():
                        target_parser = parse_page(target)
                if target_parser and parts.fragment not in target_parser.ids:
                    errors.append(f"{page.relative_to(ROOT)}: missing anchor {href}")

    card_path = ROOT / "evidence" / "run_card.json"
    try:
        card = json.loads(card_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid run-card JSON: {exc}")
        card = {}

    required = {
        "hypothesis",
        "mechanism",
        "named_non_fault_mimic",
        "holdout_dti",
        "registry_comparison",
        "raster",
        "validator",
        "submission",
        "verdict",
    }
    if not required.issubset(card):
        errors.append(f"run card missing fields: {sorted(required - card.keys())}")
    if card.get("submission", {}).get("ok_to_download") is not False:
        errors.append("run card must fail closed for download until promoted")
    if card.get("submission", {}).get("ok_to_submit") is not False:
        errors.append("run card must fail closed for submission until promoted")

    home = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").exists() else ""
    for phrase in ("OK TO DOWNLOAD: NO FILE", "OK TO SUBMIT: NO"):
        if phrase not in home:
            errors.append(f"home page does not prominently state: {phrase}")

    # A blocked run card and an unlabelled GeoTIFF must never coexist.
    if card.get("submission", {}).get("ok_to_submit") is False:
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            if path.is_file() and path.suffix.lower() in {".tif", ".tiff"}:
                errors.append(f"unapproved TIFF present while submission gate is closed: {path.relative_to(ROOT)}")

    return errors


def main() -> int:
    errors = check()
    if errors:
        print("FAIL: site/release checks found issues")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: checked {len(PAGES)} HTML pages, local links/anchors, release card, fail-closed status, and TIFF gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
