"""Config flow for the Gestion Chauffage integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_BOILER_ENTITY,
    CONF_HEATING_TYPE,
    CONF_MODE,
    DOMAIN,
    HEATING_TYPE_ELECTRIC,
    HEATING_TYPE_GAS,
    MODE_AUTO,
    MODE_AWAY,
    MODE_COMFORT,
    MODE_ECO,
)


def get_config_schema(
    suggested_values: dict[str, Any] | None = None,
) -> vol.Schema:
    """Return the configuration schema."""

    suggested_values = suggested_values or {}

    return vol.Schema(
        {
            vol.Required(
                CONF_MODE,
                default=suggested_values.get(CONF_MODE, MODE_AUTO),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        MODE_AUTO,
                        MODE_COMFORT,
                        MODE_ECO,
                        MODE_AWAY,
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                    translation_key="operating_mode",
                )
            ),
            vol.Required(
                CONF_HEATING_TYPE,
                default=suggested_values.get(
                    CONF_HEATING_TYPE,
                    HEATING_TYPE_ELECTRIC,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        HEATING_TYPE_GAS,
                        HEATING_TYPE_ELECTRIC,
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                    translation_key="heating_type",
                )
            ),
            vol.Optional(
                CONF_BOILER_ENTITY,
                description={
                    "suggested_value": suggested_values.get(
                        CONF_BOILER_ENTITY
                    )
                },
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["climate", "switch"],
                )
            ),
        }
    )


class HeatingConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Gestion Chauffage."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial configuration step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            heating_type = user_input[CONF_HEATING_TYPE]
            boiler_entity = user_input.get(CONF_BOILER_ENTITY)

            if (
                heating_type == HEATING_TYPE_GAS
                and not boiler_entity
            ):
                errors[CONF_BOILER_ENTITY] = "boiler_required"
            else:
                # Évite plusieurs configurations identiques.
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()

                # Pour le chauffage électrique, on supprime la chaudière
                # si une ancienne valeur a été transmise.
                if heating_type == HEATING_TYPE_ELECTRIC:
                    user_input.pop(CONF_BOILER_ENTITY, None)

                return self.async_create_entry(
                    title="Gestion du chauffage",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=get_config_schema(user_input),
            errors=errors,
        )
