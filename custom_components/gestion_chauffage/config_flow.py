"""Config flow for the Chauffage Intelligent integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_BOILER_ENTITY,
    CONF_HEATING_TYPE,
    CONF_MODE_SELECTOR,
    DOMAIN,
    HEATING_TYPE_ELECTRIC,
    HEATING_TYPE_GAS,
)


def _get_schema(
    user_input: dict[str, Any] | None = None,
) -> vol.Schema:
    """Return the configuration schema."""

    user_input = user_input or {}

    return vol.Schema(
        {
            vol.Required(
                CONF_MODE_SELECTOR,
                description={
                    "suggested_value": user_input.get(CONF_MODE_SELECTOR)
                },
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["input_select", "select"],
                    multiple=False,
                )
            ),
            vol.Required(
                CONF_HEATING_TYPE,
                default=user_input.get(
                    CONF_HEATING_TYPE,
                    HEATING_TYPE_ELECTRIC,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {
                            "value": HEATING_TYPE_GAS,
                            "label": "Gaz",
                        },
                        {
                            "value": HEATING_TYPE_ELECTRIC,
                            "label": "Électrique",
                        },
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_BOILER_ENTITY,
                description={
                    "suggested_value": user_input.get(CONF_BOILER_ENTITY)
                },
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["climate", "switch"],
                    multiple=False,
                )
            ),
        }
    )


class ChauffageIntelligentConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Chauffage Intelligent configuration flow."""

    VERSION = 1
    MINOR_VERSION = 1

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
                # Une seule configuration de l'intégration est autorisée.
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()

                # La chaudière n'est pas enregistrée pour un chauffage
                # électrique.
                if heating_type == HEATING_TYPE_ELECTRIC:
                    user_input.pop(CONF_BOILER_ENTITY, None)

                return self.async_create_entry(
                    title="Chauffage Intelligent",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(user_input),
            errors=errors,
        )
