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
    CONF_MODE_SELECTOR,
    DOMAIN,
    HEATING_TYPE_ELECTRIC,
    HEATING_TYPE_GAS,
)


def _get_schema(
    suggested_values: dict[str, Any] | None = None,
) -> vol.Schema:
    """Return the configuration schema."""

    suggested_values = suggested_values or {}

    return vol.Schema(
        {
            vol.Required(
                CONF_MODE_SELECTOR,
                description={
                    "suggested_value": suggested_values.get(
                        CONF_MODE_SELECTOR
                    )
                },
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["input_select", "select"],
                    multiple=False,
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
                    "suggested_value": suggested_values.get(
                        CONF_BOILER_ENTITY
                    )
                },
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["climate", "switch"],
                    multiple=False,
                )
            ),
        }
    )


def _validate_input(
    user_input: dict[str, Any],
) -> dict[str, str]:
    """Validate the configuration form."""

    errors: dict[str, str] = {}

    heating_type = user_input[CONF_HEATING_TYPE]
    boiler_entity = user_input.get(CONF_BOILER_ENTITY)

    if (
        heating_type == HEATING_TYPE_GAS
        and not boiler_entity
    ):
        errors[CONF_BOILER_ENTITY] = "boiler_required"

    return errors


def _clean_input(
    user_input: dict[str, Any],
) -> dict[str, Any]:
    """Clean configuration data before storing it."""

    cleaned_input = dict(user_input)

    if cleaned_input[CONF_HEATING_TYPE] == HEATING_TYPE_ELECTRIC:
        cleaned_input.pop(CONF_BOILER_ENTITY, None)

    return cleaned_input


class GestionChauffageConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Gestion Chauffage configuration flow."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial configuration step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            errors = _validate_input(user_input)

            if not errors:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()

                cleaned_input = _clean_input(user_input)

                return self.async_create_entry(
                    title="Gestion Chauffage",
                    data=cleaned_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(user_input),
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the integration."""

        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = _validate_input(user_input)

            if not errors:
                cleaned_input = _clean_input(user_input)

                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=cleaned_input,
                )

        suggested_values = dict(entry.data)

        if user_input is not None:
            suggested_values.update(user_input)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_get_schema(suggested_values),
            errors=errors,
        )
