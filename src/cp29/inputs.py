"""The inputs, pinned and joined by delivery hour (the packet's §0, "The joins").

- **The cleared prices:** the committed snapshot's `price_eur_mwh`, by UTC hour. A delivery day's hours are the
  snapshot's hours for that Europe/Berlin day: 23, 24 or 25.
- **v6** (A1 in the frozen records): CP-28's stored forecasts, arm `A1`, `q25`, `q50`, `q75`.
- **v5:** CP-24's committed predictions, policy `v5`, `p25`, `p50`, `p75`, folds 2–5 (P-v5).
- **The similar-day naive:** the frozen rule `delu_forecast.baselines.similar_day_naive` on the committed snapshot.
- **Perfect foresight:** the cleared prices themselves.

Every input is checked against its pinned SHA-256 before it is read, and every row against the development boundary
(`cp25.guard`, delivery days through 2026-09-06): a later row is refused, and the snapshot's rows are cut at the boundary
before anything else reads them.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from cp25 import guard

ROOT = Path(__file__).resolve().parents[2]

#: Every input, pinned by SHA-256 (the brief's execution inputs).
PINNED = {
    "docs/track-b/economic-policy-contract-2026-11-15.md":
        "21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889",
    "reports/cp28/forecast/hourly.parquet": "f5cb02a19236edd20c182c2874a5d59628652e6838fe5745aa6ffacf3f53f638",
    "reports/cp28/forecast/manifest.json": "f092140ed028d18a973bfad11ad9aa0397ad3e492223c4da683bc8e775cf3ce8",
    "reports/cp28/results/daily-losses.parquet": "7e9c972f24a99627fd7e9ed8fc80ecffbf4b50be55426805d5b574a6ede9b85d",
    "reports/ddnn2/attempt-1/predictions.parquet": "9d3f539fa78e34e65cb495a0e79f8044731e33d5b2d9e95d110a1ce886a05cf9",
    "data/snapshot.parquet": "7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00",
    "src/delu_forecast/baselines.py": "4e234cda6d09366b6136b2c2f4635dabdaa8aefe8d85ef0da41d9ad4912eea52",
    "reports/rebaseline/cold-rerun-2026-10-15/parity.json":
        "090c3cb4cbed69a9a8bdca626ce1607376e014fb3907630d525631bf7bbcdbc5",
}
#: The populations and regimes, PRES-6's (`docs/track-b/evidence/pres-6/publication-packet.md` §0).
P_ALL = ("2020-12-29", "2026-09-06")
P_V5_FOLDS = ("fold_2", "fold_3", "fold_4", "fold_5")
REGIMES = (("pre_crisis", "2020-12-29", "2021-08-31"), ("crisis", "2021-09-01", "2022-12-31"),
           ("negative_prices", "2023-01-01", "2026-09-06"))
P_ALL_DAYS, P_V5_DAYS = 2068, 358


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_pins(root: Path = ROOT) -> dict[str, str]:
    """Every pinned input's SHA-256, refusing any that differs."""
    out = {}
    for rel, pinned in PINNED.items():
        got = sha256(root / rel)
        if got != pinned:
            raise ValueError(f"{rel}: SHA-256 {got} is not the pinned {pinned}")
        out[rel] = got
    return out


def regime_of(day: str) -> str:
    return next(name for name, lo, hi in REGIMES if lo <= day <= hi)


@dataclass(frozen=True)
class Day:
    """One delivery day: its UTC hours (the snapshot's), its cleared prices, and each source's forecasts on those
    hours (NaN where the source holds none)."""
    day: str
    hours: pd.DatetimeIndex
    price: np.ndarray
    sources: dict[str, dict[str, np.ndarray]]   # source -> {"q25", "q50", "q75"} (the naive: "q50" only)


def _prices(root: Path) -> pd.DataFrame:
    s = pd.read_parquet(root / "data/snapshot.parquet", columns=["timestamp_utc", "delivery_date", "price_eur_mwh"])
    s["day"] = s.delivery_date.astype(str)
    s = s.loc[s.day <= str(guard.BOUNDARY)].copy()          # the red line: nothing after 2026-09-06 is read on
    guard.admit_rows(pd.DatetimeIndex(s.timestamp_utc).to_pydatetime())
    return s


def populations(root: Path = ROOT) -> dict[str, list[str]]:
    """P-all: CP-28's A1 days from 2020-12-29 to 2026-09-06 (2,068); P-v5: those inside v5's folds 2–5 (358)."""
    daily = pd.read_parquet(root / "reports/cp28/results/daily-losses.parquet", columns=["stream", "day"])
    p_all = sorted(set(daily.loc[(daily.stream == "A1") & daily.day.between(*P_ALL), "day"]))
    pred = pd.read_parquet(root / "reports/ddnn2/attempt-1/predictions.parquet", columns=["fold", "policy",
                                                                                         "delivery_date"])
    v5 = pred.loc[(pred.policy == "v5") & pred.fold.isin(P_V5_FOLDS), "delivery_date"].astype(str)
    p_v5 = sorted(set(v5) & set(p_all))
    if (len(p_all), len(p_v5)) != (P_ALL_DAYS, P_V5_DAYS):
        raise ValueError(f"populations {len(p_all)} and {len(p_v5)}, not PRES-6's {P_ALL_DAYS} and {P_V5_DAYS}")
    for day in p_all:
        guard.admit_delivery_day(date.fromisoformat(day))
    return {"P-all": p_all, "P-v5": p_v5}


def naive_central(root: Path = ROOT) -> pd.Series:
    """The similar-day naive's central vector by its frozen rule, from the committed snapshot (cut at the boundary)."""
    from delu_forecast.baselines import similar_day_naive

    s = _prices(root)
    return similar_day_naive(s[["timestamp_utc", "price_eur_mwh"]])


def load_days(root: Path = ROOT) -> dict[str, Day]:
    """Every P-all day, with the cleared prices and every source's forecasts joined by UTC hour."""
    check_pins(root)
    pops = populations(root)
    p_all, p_v5 = set(pops["P-all"]), set(pops["P-v5"])
    prices = _prices(root)
    prices = prices.loc[prices.day.isin(p_all)]
    hourly = pd.read_parquet(root / "reports/cp28/forecast/hourly.parquet",
                             columns=["arm", "day", "timestamp_utc", "q25", "q50", "q75"])
    a1 = hourly.loc[(hourly.arm == "A1") & hourly.day.isin(p_all)].set_index("timestamp_utc")
    pred = pd.read_parquet(root / "reports/ddnn2/attempt-1/predictions.parquet",
                           columns=["fold", "policy", "timestamp_utc", "delivery_date", "p25", "p50", "p75"])
    v5 = pred.loc[(pred.policy == "v5") & pred.fold.isin(P_V5_FOLDS)
                  & pred.delivery_date.astype(str).isin(p_v5)].set_index("timestamp_utc")
    naive = naive_central(root)
    for frame in (a1, v5):
        guard.admit_rows(pd.DatetimeIndex(frame.index).to_pydatetime())
    out: dict[str, Day] = {}
    for day, group in prices.groupby("day", sort=True):
        hours = pd.DatetimeIndex(group.timestamp_utc)
        sources = {
            "v6": {q: a1[q].reindex(hours).to_numpy(float) for q in ("q25", "q50", "q75")},
            "naive": {"q50": naive.reindex(hours.tz_convert("UTC")).to_numpy(float)},
            "perfect_foresight": {"q50": group.price_eur_mwh.to_numpy(float)},
        }
        if day in p_v5:
            sources["v5"] = {q: v5[p].reindex(hours).to_numpy(float) for q, p in (("q25", "p25"), ("q50", "p50"),
                                                                                  ("q75", "p75"))}
        out[day] = Day(day, hours, group.price_eur_mwh.to_numpy(float), sources)
    if sorted(out) != pops["P-all"]:
        raise ValueError("the snapshot does not hold every P-all day")
    return out
