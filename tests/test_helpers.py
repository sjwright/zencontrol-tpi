"""Tests for zencontrol-tpi helpers."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from custom_components.zencontrol_tpi.const import (
    SCENE_NONE,
    arc_to_brightness,
    brightness_to_arc,
    kelvin_to_mireds,
    mireds_to_kelvin,
)
from custom_components.zencontrol_tpi.manifest_store import build_manifest
from custom_components.zencontrol_tpi.rate_limiter import RateLimiter
from custom_components.zencontrol_tpi.sysvar import classify_sysvar


def test_arc_brightness_roundtrip() -> None:
    """Arc and brightness conversions are inverse-ish in the working range."""
    arc = brightness_to_arc(128)
    assert arc > 0
    brightness = arc_to_brightness(arc)
    assert 100 <= brightness <= 160


def test_kelvin_mireds_roundtrip() -> None:
    """Kelvin and mireds convert consistently within rounding."""
    mireds = kelvin_to_mireds(3000)
    assert mireds == 333
    assert abs(mireds_to_kelvin(mireds) - 3000) <= 5


def test_classify_sysvar() -> None:
    """Labels classify to sensor, switch, both, or neither."""
    assert classify_sysvar("Hallway Lux Sensor") == (True, False)
    assert classify_sysvar("MVHR Boost Switch") == (False, True)
    assert classify_sysvar("Garage Door Switch Sensor") == (True, True)
    assert classify_sysvar("Internal Flag") == (False, False)
    assert classify_sysvar(None) == (False, False)


def test_build_manifest_dedupes_sysvars() -> None:
    """Manifest stores one sysvar record with both exposure flags."""
    ctrl = SimpleNamespace(name="zen1")
    sv = SimpleNamespace(controller=ctrl, id=2, label="Lux Sensor Switch")
    hub = SimpleNamespace(
        lights=[],
        groups=[],
        buttons=[],
        motion_sensors=[],
        sv_switches=[sv],
        sv_sensors=[sv],
        profiles=[],
    )
    manifest = build_manifest(hub)
    assert len(manifest["sysvars"]) == 1
    assert manifest["sysvars"][0]["as_sensor"] is True
    assert manifest["sysvars"][0]["as_switch"] is True


@pytest.mark.asyncio
async def test_rate_limiter_execute_batch() -> None:
    """Rate limiter runs all coroutines."""
    limiter = RateLimiter(max_concurrent=2, delay_between_batches=0)
    calls: list[int] = []

    async def work(n: int) -> int:
        calls.append(n)
        return n

    results = await limiter.execute_batch([work(1), work(2), work(3)])
    assert results == [1, 2, 3]
    assert calls == [1, 2, 3]


def test_scene_none_constant() -> None:
    """Scene none label matches mqtt_bridge."""
    assert SCENE_NONE == "None"
