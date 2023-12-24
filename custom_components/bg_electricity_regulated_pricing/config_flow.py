"""Config flow for bg_electricity_regulated_pricing integration."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol
from homeassistant.const import UnitOfTime
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)

from .const import DOMAIN, PROVIDERS, CONF_PROVIDER, CONF_TARIFF_TYPE, TARIFF_TYPES, \
    CONF_CLOCK_OFFSET, CONF_CUSTOM_DAY_PRICE, CONF_CUSTOM_NIGHT_PRICE, \
    BGN_PER_KILOWATT_HOUR

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PROVIDER): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=PROVIDERS,
                translation_key=CONF_PROVIDER
            ),
        ),
        vol.Required(CONF_TARIFF_TYPE): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=TARIFF_TYPES,
                translation_key=CONF_TARIFF_TYPE
            )
        ),
        vol.Required(CONF_CLOCK_OFFSET, default=0): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=-720, max=720, mode=selector.NumberSelectorMode.BOX,
                unit_of_measurement=UnitOfTime.MINUTES
            ),
        ),
        vol.Required(CONF_CUSTOM_DAY_PRICE, default=0): selector.NumberSelector(
            selector.NumberSelectorConfig(
                step="any", mode=selector.NumberSelectorMode.BOX,
                unit_of_measurement=BGN_PER_KILOWATT_HOUR
            ),
        ),
        vol.Required(CONF_CUSTOM_NIGHT_PRICE, default=0): selector.NumberSelector(
            selector.NumberSelectorConfig(
                step="any", mode=selector.NumberSelectorMode.BOX,
                unit_of_measurement=BGN_PER_KILOWATT_HOUR
            ),
        )
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("name"): selector.TextSelector(),
    }
).extend(OPTIONS_SCHEMA.schema)

CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA)
}

OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(OPTIONS_SCHEMA)
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for bg_electricity_regulated_pricing."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return cast(str, options["name"]) if "name" in options else ""
