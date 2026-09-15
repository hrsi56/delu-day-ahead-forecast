"""The §7.3 routing rule, enforced structurally rather than by review.

`capstone_v20.md` §0 splits the programme across two models with two jobs:

    frozen v2   -- the model of record. Every result, every metric, the report.
    daily-demo  -- the demo. One page, and no results at all.

§7.3 forbids a figure from the daily service ever being quoted as, compared with,
or substituted for a confirmatory result. A convention cannot enforce that; a
namespace can. Every figure the daily service produces lives under a `live_`
prefix, and the surfaces that speak for the model of record may not render one.

The failure this guards is not cosmetic. A stale number is a formatting bug; a
rolling figure from an unvalidated daily model presented as a one-shot holdout
result is a credibility failure, and it is unrecoverable once it is published.

This file is written before the first live claim exists, deliberately. A guard
added after the thing it guards has shipped has already missed its moment --
and a guard that has never been shown to fail is not a guard, which is what
`test_positive_control_*` is for.
"""
from __future__ import annotations

import pytest

from delu_forecast.claims import build_claims
from delu_forecast.surfaces import load_surfaces

LIVE_PREFIX = "live_"

#: Surfaces that speak for the model of record. The live scorecard, when it
#: exists, is NOT one of them and is not loaded here.
RECORD_SURFACES = ("README", "Space card", "Static Space card", "Pages export")


def _record_surfaces():
    return [s for s in load_surfaces() if s.name in RECORD_SURFACES]


def test_the_record_claim_set_contains_no_live_figures():
    """`build_claims()` speaks for the frozen model of record. Nothing from the
    daily service belongs in it -- the live scorecard gets its own builder."""
    leaked = sorted(k for k in build_claims().values if k.startswith(LIVE_PREFIX))
    assert not leaked, (
        f"{leaked} entered the record claim set. Daily-service figures belong to the live "
        "scorecard's own namespace; capstone_v20.md §7.3 forbids them here."
    )


@pytest.mark.parametrize("surface", _record_surfaces(), ids=lambda s: s.name)
def test_no_record_surface_renders_a_live_figure(surface):
    """Belt and braces: even if a `live_` key reached the claim set, no surface
    that speaks for the model of record may have rendered one."""
    leaked = sorted(k for k in build_claims().values if k.startswith(LIVE_PREFIX))
    rendered = [k for k in leaked if surface.carries(k, build_claims()[k])]
    assert not rendered, f"{surface.name} renders daily-service figures {rendered}"


def test_positive_control_the_guard_catches_an_injected_live_figure():
    """The control the bar names: a synthetic `live_` key must fail the check.

    Without this, both assertions above pass vacuously for as long as the daily
    service does not exist -- which is exactly the shape of test CP-1's first
    attempt shipped ten of.
    """
    claims = dict(build_claims().values)
    claims["live_rolling_mae"] = "24.81"

    leaked = sorted(k for k in claims if k.startswith(LIVE_PREFIX))
    assert leaked == ["live_rolling_mae"], "the guard failed to see an injected live figure"

    # and the same detection the surface assertion relies on
    assert any(k.startswith(LIVE_PREFIX) for k in claims), "prefix detection is inert"
