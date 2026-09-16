"""Sensor platform for Gestion Chauffage."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    SECURITY_STATE_GRAY,
    SECURITY_STATE_GREEN,
    SECURITY_STATE_ORANGE,
    SECURITY_STATE_RED,
    SECURITY_STATES,
)
from .entity import (
    GestionChauffageEntity,
    GestionChauffageRuntimeData,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Gestion Chauffage sensor entities."""

    runtime_data: GestionChauffageRuntimeData = hass.data[DOMAIN][
        entry.entry_id
    ]["runtime_data"]

    security_sensor = EtatSecuriteChauffageSensor(
        entry,
        runtime_data,
    )

    hass.data[DOMAIN][entry.entry_id][
        "security_entities"
    ] = [security_sensor]

    async_add_entities([security_sensor])


class EtatSecuriteChauffageSensor(
    GestionChauffageEntity,
    SensorEntity,
    RestoreEntity,
):
    """Sensor exposing the heating security state."""

    _attr_name = "État de la sécurité chauffage"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = SECURITY_STATES
    _attr_translation_key = "heating_security_state"

    def __init__(
        self,
        entry: ConfigEntry,
        runtime_data: GestionChauffageRuntimeData,
    ) -> None:
        """Initialize the heating security sensor."""

        super().__init__(entry, runtime_data)

        self._attr_unique_id = (
            f"{entry.entry_id}_etat_securite_chauffage"
        )

    @property
    def native_value(self) -> str:
        """Return the current security state."""

        return self._runtime_data.security_state

    @property
    def icon(self) -> str:
        """Return an icon matching the security state."""

        icons = {
            SECURITY_STATE_GRAY: "mdi:shield-outline",
            SECURITY_STATE_GREEN: "mdi:shield-check",
            SECURITY_STATE_ORANGE: "mdi:shield-alert",
            SECURITY_STATE_RED: "mdi:shield-off",
        }

        return icons.get(
            self._runtime_data.security_state,
            "mdi:shield-outline",
        )

    async def async_added_to_hass(self) -> None:
        """Restore the previous security state."""

        await super().async_added_to_hass()

        previous_state = await self.async_get_last_state()

        if (
            previous_state is not None
            and previous_state.state in SECURITY_STATES
        ):
            self._runtime_data.security_state = (
                previous_state.state
            )
