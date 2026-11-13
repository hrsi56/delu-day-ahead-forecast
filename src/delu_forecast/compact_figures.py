"""The archived report's figures, re-encoded without loss for the page's 2.0 MB budget (PRES-5).

The seven PNG figures of v1's archive are embedded in the page as data URIs. Each original is RGBA with an alpha of 255
at every pixel, and was written by matplotlib's default encoder. This module stores the same pixels as RGB and picks,
per figure, the smallest of a few standard PNG encodings: Pillow's optimizer, and an encoder that tries each PNG row
filter and two zlib strategies. Every output decodes to exactly the original's pixels; nothing is resized, quantized or
redrawn. The originals stay committed and unchanged; the page embeds the copies under `reports/pres5/compact-figures/`.

The copies are committed assets, not rebuilt by `scripts/rebuild_presentation.py`: zlib's bytes can differ between
builds of the library, while the pixels cannot. `check()` (and `tests/test_50_pres5_publication.py`) decodes each copy
and its original and requires equal pixels, an opaque original, and a copy no larger than the original.

Run ``python -m delu_forecast.compact_figures`` to write the copies, or ``--check`` to verify them.
"""
from __future__ import annotations

import argparse
import io
import json
import struct
import sys
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path("reports/pres5/compact-figures")
#: The originals, as the archive names them (`scripts/build_pages.py::ARCHIVE_FIGURES`).
ORIGINALS = (
    "reports/fig_welch_periodogram.png",
    "reports/fig_per_regime_periodogram.png",
    "reports/fig_acf_24_168.png",
    "reports/cp2/fig_shap_summary.png",
    "reports/cp2/fig_shap_dependence_price_lag_24h.png",
    "reports/cp2/fig_shap_dependence_price_lag_168h.png",
    "reports/cp2/fig_reliability_three_stage.png",
)


def pixels(data: bytes) -> np.ndarray:
    from PIL import Image

    image = Image.open(io.BytesIO(data))
    image.load()
    return np.asarray(image.convert("RGBA"))


def _chunk(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)


def _filtered(rgb: np.ndarray, kind: int) -> np.ndarray:
    """PNG filter `kind` (0 none, 1 sub, 2 up, 3 average, 4 Paeth) applied to every row, three bytes per pixel."""
    height = rgb.shape[0]
    raw = rgb.reshape(height, -1).astype(np.int16)
    up = np.vstack([np.zeros((1, raw.shape[1]), np.int16), raw[:-1]])
    left = np.hstack([np.zeros((height, 3), np.int16), raw[:, :-3]])
    corner = np.hstack([np.zeros((height, 3), np.int16), up[:, :-3]])
    if kind == 0:
        out = raw
    elif kind == 1:
        out = raw - left
    elif kind == 2:
        out = raw - up
    elif kind == 3:
        out = raw - (left + up) // 2
    else:
        guess = left + up - corner
        a, b, c = np.abs(guess - left), np.abs(guess - up), np.abs(guess - corner)
        out = raw - np.where((a <= b) & (a <= c), left, np.where(b <= c, up, corner))
    return (out % 256).astype(np.uint8)


def _searched(rgb: np.ndarray) -> bytes:
    """The smallest of: each single filter for every row, or the per-row minimum-sum heuristic; each compressed with
    zlib level 9 under the default and the filtered strategies."""
    height, width = rgb.shape[:2]
    rows = [_filtered(rgb, kind) for kind in range(5)]
    score = np.vstack([np.abs(row.astype(np.int8).astype(np.int16)).sum(axis=1) for row in rows])
    plans = [np.argmin(score, axis=0)] + [np.full(height, kind) for kind in range(5)]
    best = None
    for plan in plans:
        stream = b"".join(bytes([int(plan[i])]) + rows[int(plan[i])][i].tobytes() for i in range(height))
        for strategy in (zlib.Z_DEFAULT_STRATEGY, zlib.Z_FILTERED):
            packer = zlib.compressobj(9, zlib.DEFLATED, 15, 9, strategy)
            body = packer.compress(stream) + packer.flush()
            if best is None or len(body) < len(best):
                best = body
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) + _chunk(b"IDAT", best) + _chunk(b"IEND", b"")


def compact(original: bytes) -> bytes:
    """The smallest pixel-identical RGB encoding of an opaque RGBA original."""
    from PIL import Image

    rgba = pixels(original)
    if not (rgba[..., 3] == 255).all():
        raise ValueError("the original is not opaque at every pixel; dropping its alpha would change it")
    rgb = np.ascontiguousarray(rgba[..., :3])
    buffer = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buffer, "PNG", optimize=True)
    candidates = [buffer.getvalue(), _searched(rgb)]
    out = min(candidates, key=len)
    if not np.array_equal(pixels(out), rgba):
        raise ValueError("the re-encoded figure's pixels differ from the original's")
    return out


def copy_path(original: str) -> Path:
    return OUT / Path(original).name


def check(root: Path = ROOT) -> list[str]:
    """Why a committed copy does not stand for its original; empty when every copy does."""
    problems = []
    for original in ORIGINALS:
        source, copy = (root / original).read_bytes(), root / copy_path(original)
        if not copy.exists():
            problems.append(f"{copy_path(original)} is missing")
            continue
        theirs, ours = pixels(source), pixels(copy.read_bytes())
        if not (theirs[..., 3] == 255).all():
            problems.append(f"{original} is not opaque at every pixel")
        if theirs.shape != ours.shape or not np.array_equal(theirs, ours):
            problems.append(f"{copy_path(original)}: its pixels differ from {original}")
        if copy.stat().st_size > len(source):
            problems.append(f"{copy_path(original)} is larger than {original}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify the committed copies; write nothing")
    args = ap.parse_args(argv)
    if args.check:
        problems = check()
        print(json.dumps({"pixel_identical": not problems, "problems": problems}))
        return 0 if not problems else 13
    (ROOT / OUT).mkdir(parents=True, exist_ok=True)
    sizes = {}
    for original in ORIGINALS:
        data = compact((ROOT / original).read_bytes())
        (ROOT / copy_path(original)).write_bytes(data)
        sizes[original] = [len((ROOT / original).read_bytes()), len(data)]
    print(json.dumps({"wrote": sizes}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
