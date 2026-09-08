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


def next_number(document_xml: str) -> int:
    """One past the highest leading integer among existing Heading2 paragraphs."""
    numbers = []
    for para in re.findall(r"<w:p>.*?</w:p>", document_xml, re.S):
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
    if "<w:sectPr>" not in xml:
        sys.exit("error: no <w:sectPr> in word/document.xml — unexpected layout")

    number = next_number(xml)
    block = _rule() + _heading(f"{number}. {question}") + "".join(_para(a) for a in answers)
    xml = xml.replace("<w:sectPr>", block + "<w:sectPr>", 1)
    blobs["word/document.xml"] = xml.encode("utf-8")

    backup = docx.with_suffix(docx.suffix + ".bak")
    shutil.copy2(docx, backup)
    try:
        with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zf:
            for name in names:  # original order preserved
                zf.writestr(name, blobs[name])
    except Exception:
        shutil.copy2(backup, docx)
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
