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


# ---------------------------------------------------------------------------------------------------------------
# CP-18b: the live claim builder exists now (`cp18.live_claims`), so the wall is checked against it, not only
# against an injected key. The final-product Space renders its status, badges, wording and limitations from it.

def _live_claims():
    from cp18.live_claims import build_live_claims
    return build_live_claims(rehearsal_days=("2026-08-31", "2026-09-05"))


def test_the_live_claim_builder_speaks_only_in_the_live_namespace():
    values = _live_claims()["values"]
    assert values, "the live claim builder returned nothing"
    assert all(k.startswith(LIVE_PREFIX) for k in values), sorted(k for k in values if not k.startswith(LIVE_PREFIX))


def test_no_live_claim_key_reaches_the_record_claim_set():
    record = set(build_claims().values)
    assert not record & set(_live_claims()["values"])


@pytest.mark.parametrize("surface", _record_surfaces(), ids=lambda s: s.name)
def test_no_record_surface_renders_a_live_claim(surface):
    """Every sentence and figure the live builder produces is absent from the surfaces of the model of record."""
    rendered = sorted(k for k, v in _live_claims()["values"].items() if surface.carries(k, v))
    assert not rendered, f"{surface.name} renders live claims {rendered}"


def test_the_shared_claims_are_record_claims_unchanged():
    """What the live Space reuses from the record layer is the record's own text, by its own key, verbatim."""
    import delu_forecast.claims as record
    from cp18.live_claims import SHARED, SHARED_CONSTANTS
    shared = _live_claims()["shared"]
    claims = build_claims()
    for key in SHARED:
        assert shared[key] == claims[key] and not key.startswith(LIVE_PREFIX)
    for key, name in SHARED_CONSTANTS.items():
        assert shared[key] == getattr(record, name)


def test_positive_control_the_surface_check_catches_a_live_claim_on_a_record_surface():
    """A copy of a record surface that carries one live sentence must be caught by the same `carries` check."""
    from dataclasses import replace
    surface = _record_surfaces()[0]
    key, value = "live_limitation_rehearsal", _live_claims()["values"]["live_limitation_rehearsal"]
    assert not surface.carries(key, value)
    tainted = replace(surface, text=surface.text + " " + value)
    assert tainted.carries(key, value), "the surface check cannot see a live claim"
