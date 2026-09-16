"""The Chauffage Intelligent integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BOILER_ENTITY,
    CONF_HEATING_TYPE,
    CONF_MODE_SELECTOR,
    DOMAIN,
)


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up the integration from YAML."""

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Chauffage Intelligent from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_MODE_SELECTOR: entry.data[CONF_MODE_SELECTOR],
        CONF_HEATING_TYPE: entry.data[CONF_HEATING_TYPE],
        CONF_BOILER_ENTITY: entry.data.get(CONF_BOILER_ENTITY),
    }

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        if not hass.datahass.data.pop(DOMAIN, None)

    return True
