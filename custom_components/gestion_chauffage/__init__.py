"""The Gestion Chauffage integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BOILER_ENTITY,
    CONF_HEATING_TYPE,
    CONF_MODE_SELECTOR,
    DOMAIN,
    PLATFORMS,
)
from .entity import GestionChauffageRuntimeData


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up Gestion Chauffage from YAML."""

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Gestion Chauffage from a config entry."""

    runtime_data = GestionChauffageRuntimeData()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "runtime_data": runtime_data,
        CONF_MODE_SELECTOR: entry.data[CONF_MODE_SELECTOR],
        CONF_HEATING_TYPE: entry.data[CONF_HEATING_TYPE],
        CONF_BOILER_ENTITY: entry.data.get(CONF_BOILER_ENTITY),
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        if not hass.datahass.data.pop(DOMAIN, None)

    return unload_ok
