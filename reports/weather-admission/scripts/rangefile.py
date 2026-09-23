"""Seekable read-only file object backed by metered HTTP range reads."""

from __future__ import annotations

import io

from net import fetch


class RangeFile(io.RawIOBase):
    """Minimal file-like object: every read becomes one metered Range request.

    Reads are cached by exact (offset, length) blocks aligned to ``block``
    so that zipfile's small header reads do not each cost a round trip.
    """

    def __init__(self, url: str, size: int, purpose: str, *, auth_hf: bool = False, block: int = 65536):
        self.url, self.size, self.purpose, self.auth_hf, self.block = url, size, purpose, auth_hf, block
        self.pos = 0
        self._cache: dict[int, bytes] = {}

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def _get(self, start: int, end: int) -> bytes:
        status, _, body = fetch(self.url, self.purpose, byte_range=(start, end - 1), auth_hf=self.auth_hf)
        if status not in (200, 206) or len(body) != end - start:
            raise OSError(f"range read failed: status={status} got={len(body)} want={end - start}")
        return body

    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            n = self.size - self.pos
        n = max(0, min(n, self.size - self.pos))
        if n == 0:
            return b""
        start, end = self.pos, self.pos + n
        if n > 4 * self.block:
            data = self._get(start, end)
        else:
            b0 = start // self.block
            b1 = (end - 1) // self.block
            parts = []
            for bi in range(b0, b1 + 1):
                if bi not in self._cache:
                    bs = bi * self.block
                    self._cache[bi] = self._get(bs, min(bs + self.block, self.size))
                parts.append(self._cache[bi])
            buf = b"".join(parts)
            off = start - b0 * self.block
            data = buf[off : off + n]
        self.pos = end
        return data

    def readinto(self, b) -> int:
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)
