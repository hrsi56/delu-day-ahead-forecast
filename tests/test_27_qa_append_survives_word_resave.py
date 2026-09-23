"""`scripts/qa_append.py` must work on the Q&A document as Word actually saves it.

The defect this guards, found 2026-09-17. The Q&A document is formatted by hand in
Word, deliberately — agents write content, the owner owns presentation. Word
re-saves every paragraph with revision ids: `<w:p w:rsidR="...">`, and the body's
section properties as `<w:sectPr w:rsidR="...">`. The tool matched the literal tags
`<w:p>` and `<w:sectPr>`, so on the real document it:

  * refused to run at all — `error: no <w:sectPr>` — so nothing could be filed; and
  * saw 0 of 30 headings, so with that guard loosened it would have numbered the
    next entry `1.` silently.

Meanwhile two entries filed to an older, never-re-saved copy on a review branch
were stranded when the formatted file was adopted. Both failures came from two
correct rules colliding: never hand-edit the `.docx`, and presentation is the
owner's.

The fixture below is synthetic but carries the exact shapes Word writes. The
positive controls prove it: the old matching logic is shown to be blind to this
fixture, so these tests cannot pass against the defective tool.
"""
from __future__ import annotations

import re
import zipfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "qa_append.py"

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

#: Word-shaped document: revision ids on paragraphs, runs and sectPr; a heading
#: split across two runs; and an earlier section break whose sectPr sits inside a
#: paragraph's pPr — so "the first sectPr" is the wrong place to splice.
WORD_XML = (
    f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
    '<w:p w:rsidR="00A1B2C3" w:rsidRDefault="00A1B2C3"><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    '<w:r w:rsidR="00D4E5F6"><w:t xml:space="preserve">1. </w:t></w:r><w:r><w:t>ראשונה</w:t></w:r></w:p>'
    '<w:p w:rsidR="00A1B2C3"><w:pPr><w:bidi/></w:pPr><w:r><w:t>תשובה</w:t></w:r></w:p>'
    '<w:p w:rsidR="00A1B2C3"><w:pPr><w:sectPr w:rsidR="00EEEEEE"><w:type w:val="continuous"/></w:sectPr></w:pPr></w:p>'
    '<w:p w:rsidR="00A1B2C3"><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:t>2. שנייה</w:t></w:r></w:p>'
    '<w:sectPr w:rsidR="00391D6C"><w:pgSz w:w="11906" w:h="16838"/></w:sectPr>'
    "</w:body></w:document>"
)
OTHER_PARTS = {
    "[Content_Types].xml": b'<?xml version="1.0"?><Types/>',
    "word/styles.xml": b'<?xml version="1.0"?><w:styles/>',
}


def _load():
    spec = spec_from_file_location("qa_append", SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make(path: Path, xml: str = WORD_XML) -> Path:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("word/document.xml", xml)
        for name, blob in OTHER_PARTS.items():
            zf.writestr(name, blob)
    return path


def _parts(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as zf:
        return {name: zf.read(name) for name in zf.namelist()}


def _headings(xml: str) -> list[int]:
    found = []
    for para in re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", xml, re.S):
        if 'w:val="Heading2"' in para:
            m = re.match(r"\s*(\d+)", "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S)))
            if m:
                found.append(int(m.group(1)))
    return found


@pytest.fixture
def qa(tmp_path):
    module = _load()
    module.BACKUP_DIR = tmp_path / "bak"  # never write into the real project .local/
    return module


# -- positive controls: the fixture really does defeat the old logic ----------------


def test_positive_control_the_old_paragraph_match_is_blind_to_word_output():
    old = [p for p in re.findall(r"<w:p>.*?</w:p>", WORD_XML, re.S) if 'w:val="Heading2"' in p]
    assert old == [], "the fixture no longer carries Word's attributed paragraphs"
    assert _headings(WORD_XML) == [1, 2]


def test_positive_control_the_old_sectpr_check_fails_on_word_output():
    assert "<w:sectPr>" not in WORD_XML, "the fixture no longer carries Word's attributed sectPr"


# -- the fix -------------------------------------------------------------------------


def test_numbers_from_word_headings_including_a_heading_split_across_runs(qa, tmp_path):
    doc = _make(tmp_path / "doc.docx")
    assert qa.append_entry(doc, "שאלה", ["תשובה"]) == 3
    assert _headings(_parts(doc)["word/document.xml"].decode()) == [1, 2, 3]


def test_the_change_is_a_pure_insertion_before_the_body_level_sectpr(qa, tmp_path):
    doc = _make(tmp_path / "doc.docx")
    qa.append_entry(doc, "שאלה", ["תשובה"])
    after = _parts(doc)["word/document.xml"].decode()
    cut = WORD_XML.rindex('<w:sectPr w:rsidR="00391D6C">')
    assert after.startswith(WORD_XML[:cut]) and after.endswith(WORD_XML[cut:])
    assert after.index("3. ") > after.index('w:rsidR="00EEEEEE"'), "spliced at the mid-document section break"


def test_every_other_part_is_byte_identical(qa, tmp_path):
    doc = _make(tmp_path / "doc.docx")
    qa.append_entry(doc, "שאלה", ["תשובה"])
    after = _parts(doc)
    assert {k: after[k] for k in OTHER_PARTS} == OTHER_PARTS


def test_a_wrong_number_is_refused_and_the_file_restored(qa, tmp_path):
    doc = _make(tmp_path / "doc.docx")
    before = doc.read_bytes()
    qa.next_number = lambda xml: 1  # the silent failure the old tool would have produced
    with pytest.raises(RuntimeError, match=r"numbered #1, next free number is #3"):
        qa.append_entry(doc, "שאלה", ["תשובה"])
    assert doc.read_bytes() == before
    assert not list((tmp_path / "bak").glob("*.bak")), "a restored write left its backup behind"


def test_unreadable_headings_are_refused_rather_than_numbered_one(qa, tmp_path):
    doc = _make(tmp_path / "doc.docx", WORD_XML.replace("<w:p ", "<w:pX "))
    with pytest.raises(SystemExit, match="refusing"):
        qa.append_entry(doc, "שאלה", ["תשובה"])


def test_a_document_that_really_is_empty_starts_at_one(qa, tmp_path):
    empty = f'<?xml version="1.0"?><w:document {W}><w:body><w:sectPr w:rsidR="1"/></w:body></w:document>'
    empty = empty.replace('<w:sectPr w:rsidR="1"/>', '<w:sectPr w:rsidR="1"></w:sectPr>')
    doc = _make(tmp_path / "empty.docx", empty)
    assert qa.append_entry(doc, "שאלה", ["תשובה"]) == 1
