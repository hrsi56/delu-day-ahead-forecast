#!/usr/bin/env python3
"""Append one interview Q&A entry to the Hebrew Q&A .docx.

Stdlib only — no python-docx, no npm, no LibreOffice. Opens the .docx as the
ZIP it is, splices new paragraphs into word/document.xml before <w:sectPr>,
and rewrites the archive. RTL markup (<w:bidi/>, <w:rtl/>, right alignment)
matches what the document already uses, so appended entries render like the
hand-authored ones.

Question numbering is derived from the Heading2 paragraphs already present,
so entries stay in sequence without the caller tracking a counter.

Inline **bold** markers in the question and in each answer paragraph are
converted to bold runs. Everything else is literal text.

Usage:
    python3 scripts/qa_append.py \
        -q "איך שלפתם את הנתונים ההיסטוריים?" \
        -a "פסקת תשובה ראשונה, עם **הדגשה** במידת הצורך." \
        -a "פסקת תשובה שנייה."

Governed by AGENTS.md § Interview-answer capture. The Orchestrator files
entries; a Track B agent names a trigger in its terminal return instead.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

DEFAULT_DOCX = Path(__file__).resolve().parents[1] / "שאלות תשובות.docx"
#: Recovery backups stay inside the project, per AGENTS.md § Project-local working files.
BACKUP_DIR = Path(__file__).resolve().parents[1] / ".local" / "tmp"

FONTS = '<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
RTL = "<w:rtl/>"


def _run(text: str, *, bold: bool = False, heading: bool = False) -> str:
    """One <w:r>. Bold uses both w:b and w:bCs so it applies to Hebrew too."""
    props = [FONTS]
    if bold:
        props.append("<w:b/><w:bCs/>")
    if heading:
        props.append('<w:color w:val="2A4B7C"/><w:sz w:val="26"/><w:szCs w:val="26"/>')
    props.append(RTL)
    return (
        f"<w:r><w:rPr>{''.join(props)}</w:rPr>"
        f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    )


def _runs(text: str, *, heading: bool = False) -> str:
    """Split on **bold** markers into alternating plain/bold runs."""
    parts = re.split(r"\*\*(.+?)\*\*", text)
    out = []
    for i, part in enumerate(parts):
        if part:
            out.append(_run(part, bold=(i % 2 == 1), heading=heading))
    return "".join(out)


def _rule() -> str:
    return (
        "<w:p><w:pPr>"
        '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="C8C8C8"/></w:pBdr>'
        '<w:bidi/><w:spacing w:after="240" w:before="80"/>'
        "</w:pPr></w:p>"
    )


def _heading(text: str) -> str:
    return (
        "<w:p><w:pPr>"
        '<w:pStyle w:val="Heading2"/><w:bidi/>'
        '<w:spacing w:after="160" w:before="360"/><w:jc w:val="right"/>'
        f"</w:pPr>{_runs(text, heading=True)}</w:p>"
    )


def _para(text: str) -> str:
    return (
        "<w:p><w:pPr>"
        '<w:bidi/><w:spacing w:after="160" w:line="300"/><w:jc w:val="right"/>'
        f"</w:pPr>{_runs(text)}</w:p>"
    )


#: A paragraph opening tag with or without attributes. Word stamps revision ids
#: (`<w:p w:rsidR="...">`) on every paragraph it saves, so a literal `<w:p>` stops
#: matching the moment the document is opened and re-saved by hand. `(?:\s[^>]*)?`
#: accepts both forms and still excludes `<w:pPr>`, `<w:pStyle>` and `<w:pBdr>`.
_PARA = re.compile(r"<w:p(?:\s[^>]*)?>.*?</w:p>", re.S)
_SECTPR = re.compile(r"<w:sectPr(?:\s[^>]*)?>")


def _headings(document_xml: str) -> list[int]:
    numbers = []
    for para in _PARA.findall(document_xml):
        if 'w:val="Heading2"' not in para:
            continue
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S))
        match = re.match(r"\s*(\d+)", text)
        if match:
            numbers.append(int(match.group(1)))
    return numbers


def next_number(document_xml: str) -> int:
    """One past the highest leading integer among existing Heading2 paragraphs."""
    numbers = []
    for para in _PARA.findall(document_xml):
        if 'w:val="Heading2"' not in para:
            continue
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S))
        match = re.match(r"\s*(\d+)", text)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def append_entry(docx: Path, question: str, answers: list[str]) -> int:
    if not docx.exists():
        sys.exit(f"error: {docx} does not exist")

    with zipfile.ZipFile(docx) as zf:
        names = zf.namelist()
        blobs = {name: zf.read(name) for name in names}

    xml = blobs["word/document.xml"].decode("utf-8")
    sects = list(_SECTPR.finditer(xml))
    if not sects:
        sys.exit("error: no <w:sectPr> in word/document.xml — unexpected layout")
    before = _headings(xml)
    if not before:
        # Refuse rather than number from 1. A document with entries in it whose
        # headings cannot be read is a parsing failure, not an empty document.
        if 'w:val="Heading2"' in xml:
            sys.exit("error: Heading2 paragraphs present but unreadable — refusing to guess a number")

    number = next_number(xml)
    block = _rule() + _heading(f"{number}. {question}") + "".join(_para(a) for a in answers)
    # The body-level section properties are the last <w:sectPr> in the body. Section
    # breaks put earlier ones inside <w:pPr>; splicing before those would land the
    # entry mid-document.
    cut = sects[-1].start()
    xml = xml[:cut] + block + xml[cut:]
    blobs["word/document.xml"] = xml.encode("utf-8")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / (docx.name + ".bak")
    shutil.copy2(docx, backup)
    try:
        with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zf:
            for name in names:  # original order preserved
                zf.writestr(name, blobs[name])
        with zipfile.ZipFile(docx) as zf:
            after = _headings(zf.read("word/document.xml").decode("utf-8"))
        # Two different failures, reported as what they are. A wrong number sorts to
        # the front of the list, so comparing tails would print identical values and
        # read as a false alarm.
        want = max(before, default=0) + 1
        if number != want:
            raise RuntimeError(f"post-write check failed: numbered #{number}, next free number is #{want}")
        if sorted(after) != sorted(before + [number]):
            raise RuntimeError(
                f"post-write check failed: expected {len(before) + 1} headings ending at #{want}, "
                f"found {len(after)} ending at #{max(after, default=0)}"
            )
    except Exception:
        shutil.copy2(backup, docx)  # if this raises, the backup survives as the only good copy
        backup.unlink()
        raise
    backup.unlink()
    return number


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-q", "--question", required=True, help="the question, as a hiring manager would ask it")
    ap.add_argument("-a", "--answer", required=True, action="append", metavar="PARA",
                    help="one answer paragraph; repeat for multiple paragraphs")
    ap.add_argument("-f", "--file", type=Path, default=DEFAULT_DOCX, help="target .docx")
    args = ap.parse_args()

    number = append_entry(args.file, args.question, args.answer)
    print(f"appended entry {number} to {args.file}")


if __name__ == "__main__":
    main()
