"""Switch platform for zencontrol-tpi (ZenSystemVariable switch type)."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ZenHub, ZencontrolTpiConfigEntry
from .entity import ZenControllerEntity, controller_device_info

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ZencontrolTpiConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up switch entities after discovery completes."""
    hub = entry.runtime_data

    async def on_discovery() -> None:
        entities = [
            ZenSystemVariableSwitchEntity(hub, sv) for sv in hub.sv_switches
        ]
        if entities:
            async_add_entities(entities)

    hub.register_discovery_callback(on_discovery)


class ZenSystemVariableSwitchEntity(ZenControllerEntity, SwitchEntity):
    """HA switch entity wrapping a boolean ZenSystemVariable."""

    def __init__(self, hub: ZenHub, zen_sv: Any) -> None:
        super().__init__(hub)
        self._sv = zen_sv
        ctrl = zen_sv.controller

        self._attr_unique_id = f"{ctrl.name}_sv{zen_sv.id}_switch"
        self._suggested_object_id = f"sv{zen_sv.id}"
        self._attr_device_info = controller_device_info(ctrl)
        self._attr_name = zen_sv.label or f"System Variable {zen_sv.id}"
        self._attr_is_on = (zen_sv.value or 0) != 0

        hub.register_sv_switch_entity(zen_sv, self)

    def update_value(self, value: int) -> None:
        """Called by ZenHub when the system variable changes."""
        self._attr_is_on = value != 0
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._sv.set_value(1)
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._sv.set_value(0)
        self._attr_is_on = False
