"""Switch platform for Gestion Chauffage."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN
from .entity import (
    GestionChauffageEntity,
    GestionChauffageRuntimeData,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Gestion Chauffage switch entities."""

    runtime_data: GestionChauffageRuntimeData = hass.data[DOMAIN][
        entry.entry_id
    ]["runtime_data"]

    async_add_entities(
        [
            ChauffageGeneralSwitch(
                entry,
                runtime_data,
            )
        ]
    )


class ChauffageGeneralSwitch(
    GestionChauffageEntity,
    SwitchEntity,
    RestoreEntity,
):
    """Switch controlling the general heating state."""

    _attr_name = "Chauffage général"
    _attr_icon = "mdi:radiator"
    _attr_translation_key = "general_heating"

    def __init__(
        self,
        entry: ConfigEntry,
        runtime_data: GestionChauffageRuntimeData,
    ) -> None:
        """Initialize the heating switch."""

        super().__init__(entry, runtime_data)

        self._attr_unique_id = (
            f"{entry.entry_id}_chauffage_general"
        )

    @property
    def is_on(self) -> bool:
        """Return whether general heating is enabled."""

        return self._runtime_data.heating_enabled

    async def async_added_to_hass(self) -> None:
        """Restore the previous heating state."""

        await super().async_added_to_hass()

        previous_state = await self.async_get_last_state()

        if previous_state is not None:
            self._runtime_data.heating_enabled = (
                previous_state.state == "on"
            )

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on general heating."""

        self._runtime_data.heating_enabled = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off general heating."""

        self._runtime_data.heating_enabled = False
        self.async_write_ha_state()
