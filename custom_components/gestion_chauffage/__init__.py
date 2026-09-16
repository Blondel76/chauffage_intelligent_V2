"""The Gestion Chauffage integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up the integration."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Gestion Chauffage from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "mode": entry.data["mode"],
        "heating_type": entry.data["heating_type"],
        "boiler_entity": entry.data.get("boiler_entity"),
    }

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        if not hass.datahass.data.pop(DOMAIN)

    return True
