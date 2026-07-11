"""Constants for the zencontrol-tpi integration."""

from __future__ import annotations

import math
from typing import Final

DOMAIN: Final = "zencontrol_tpi"

DEFAULT_PORT: Final = 5108

PLATFORMS: Final = ["light", "binary_sensor", "switch", "sensor", "select", "event"]

# Config entry keys
CONF_CONTROLLERS: Final = "controllers"
CONF_MAC: Final = "mac"
CONF_LABEL: Final = "label"
CONF_NAME: Final = "name"
CONF_UNICAST: Final = "unicast"

# Group scene select when members are discoordinated (mqtt_bridge convention)
SCENE_NONE: Final = "None"

# Logarithmic arc↔brightness constants (from mqtt_bridge)
_LOG_A: Final = -59.53
_LOG_B: Final = 56.58

# Tracks config-entry reloads that should force full bus discovery
FORCE_FULL_DISCOVERY: dict[str, bool] = {}


def arc_to_brightness(arc: int) -> int:
    """Convert DALI arc level (0-254) to HA brightness (0-255)."""
    if arc <= 0:
        return 0
    return min(255, round(math.exp((arc - _LOG_A) / _LOG_B)))


def brightness_to_arc(brightness: int) -> int:
    """Convert HA brightness (0-255) to DALI arc level (0-254)."""
    if brightness <= 0:
        return 0
    return min(254, max(0, round(_LOG_A + _LOG_B * math.log(brightness))))


def kelvin_to_mireds(kelvin: int) -> int:
    """Convert Kelvin to mireds."""
    if kelvin <= 0:
        return 0
    return round(1_000_000 / kelvin)


def mireds_to_kelvin(mireds: int) -> int:
    """Convert mireds to Kelvin."""
    if mireds <= 0:
        return 0
    return round(1_000_000 / mireds)
