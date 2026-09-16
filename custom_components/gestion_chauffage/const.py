"""Constants for the Gestion Chauffage integration."""

from homeassistant.const import Platform

DOMAIN = "gestion_chauffage"

PLATFORMS: list[Platform] = [
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.SENSOR,
]

CONF_MODE_SELECTOR = "mode_selector"
CONF_HEATING_TYPE = "heating_type"
CONF_BOILER_ENTITY = "boiler_entity"

HEATING_TYPE_GAS = "gas"
HEATING_TYPE_ELECTRIC = "electric"

SECURITY_STATE_GRAY = "gris"
SECURITY_STATE_GREEN = "vert"
SECURITY_STATE_ORANGE = "orange"
SECURITY_STATE_RED = "rouge"

SECURITY_STATES = [
    SECURITY_STATE_GRAY,
    SECURITY_STATE_GREEN,
    SECURITY_STATE_ORANGE,
    SECURITY_STATE_RED,
]
