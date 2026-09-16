"""Base entities and runtime data for Gestion Chauffage."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SECURITY_STATE_GRAY


@dataclass
class GestionChauffageRuntimeData:
    """Runtime data shared by Gestion Chauffage entities."""

    heating_enabled: bool = False
    security_state: str = SECURITY_STATE_GRAY


class GestionChauffageEntity(Entity):
    """Base class for Gestion Chauffage entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        runtime_data: GestionChauffageRuntimeData,
    ) -> None:
        """Initialize the base entity."""

        self._entry = entry
        self._runtime_data = runtime_data

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gestion Chauffage",
            manufacturer="Blondel76",
            model="Chauffage Intelligent",
        )
``
