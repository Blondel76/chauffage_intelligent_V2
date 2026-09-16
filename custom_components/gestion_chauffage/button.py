"""Button platform for Gestion Chauffage."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN, SECURITY_STATE_GREEN
from .entity import (
    GestionChauffageEntity,
    GestionChauffageRuntimeData,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Gestion Chauffage button entities."""

    runtime_data: GestionChauffageRuntimeData = hass.data[DOMAIN][
        entry.entry_id
    ]["runtime_data"]

    async_add_entities(
        [
            RearmementSecuriteButton(
                entry,
                runtime_data,
            )
        ]
    )


class RearmementSecuriteButton(
    GestionChauffageEntity,
    ButtonEntity,
):
    """Button used to reset heating security."""

    _attr_name = "Réarmement sécurité chauffage"
    _attr_icon = "mdi:restart-alert"
    _attr_translation_key = "reset_heating_security"

    def __init__(
        self,
        entry: ConfigEntry,
        runtime_data: GestionChauffageRuntimeData,
    ) -> None:
        """Initialize the security reset button."""

        super().__init__(entry, runtime_data)

        self._attr_unique_id = (
            f"{entry.entry_id}_rearmement_securite"
        )

    async def async_press(self) -> None:
        """Reset the heating security state."""

        self._runtime_data.security_state = SECURITY_STATE_GREEN

        for entity in self.hass.data[DOMAIN][
            self._entry.entry_id
        ].get("security_entities", []):
            entity.async_write_ha_state()
