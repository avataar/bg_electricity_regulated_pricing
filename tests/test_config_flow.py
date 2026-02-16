"""Test the bg_electricity_regulated_pricing config flow."""
from unittest.mock import AsyncMock

from homeassistant import config_entries
from homeassistant.components.sensor import SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bg_electricity_regulated_pricing.const import DOMAIN


async def test_config_flow_required(
        hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test the config flow with only the required options set."""
    provider = "electrohold"
    tariff_type = "dual"
    clock_offset = 0
    custom_day_price = 0
    custom_night_price = 0

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "My Provider",
            "provider": provider,
            "tariff_type": tariff_type,
            "clock_offset": clock_offset,
            "custom_day_price": custom_day_price,
            "custom_night_price": custom_night_price
        },
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "My Provider"
    assert result["data"] == {}
    assert result["options"] == {
        "name": "My Provider",
        "provider": provider,
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": False
    }
    assert len(mock_setup_entry.mock_calls) == 1

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert config_entry.data == {}
    assert config_entry.options == {
        "name": "My Provider",
        "provider": provider,
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": False
    }
    assert config_entry.title == "My Provider"


async def test_config_flow_all(
        hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test the config flow with all options set."""
    provider = "custom"
    tariff_type = "dual"
    clock_offset = 30
    custom_day_price = 0.25
    custom_night_price = 0.15

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "My Provider",
            "provider": provider,
            "tariff_type": tariff_type,
            "clock_offset": clock_offset,
            "custom_day_price": custom_day_price,
            "custom_night_price": custom_night_price,
            "use_legacy_day_night_algorithm": True
        },
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "My Provider"
    assert result["data"] == {}
    assert result["options"] == {
        "name": "My Provider",
        "provider": provider,
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": True
    }
    assert len(mock_setup_entry.mock_calls) == 1

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert config_entry.data == {}
    assert config_entry.options == {
        "name": "My Provider",
        "provider": provider,
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": True
    }
    assert config_entry.title == "My Provider"


def get_suggested(schema, key):
    """Get suggested value for key in voluptuous schema."""
    for k in schema:
        if k == key:
            if k.description is None or "suggested_value" not in k.description:
                return None
            return k.description["suggested_value"]
    # Wanted key absent from schema
    raise Exception


async def test_options(hass: HomeAssistant) -> None:
    """Test reconfiguring."""
    provider = "electrohold"
    tariff_type = "dual"
    clock_offset = 0
    custom_day_price = 0
    custom_night_price = 0

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            "name": "My Provider",
            "provider": provider,
            "tariff_type": tariff_type,
            "clock_offset": clock_offset,
            "custom_day_price": custom_day_price,
            "custom_night_price": custom_night_price
        },
        title="My Provider",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"
    schema = result["data_schema"].schema
    assert get_suggested(schema, "provider") == "electrohold"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            "provider": "evn",
            "tariff_type": tariff_type,
            "clock_offset": clock_offset,
            "custom_day_price": custom_day_price,
            "custom_night_price": custom_night_price,
            "use_legacy_day_night_algorithm": True
        },
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "name": "My Provider",
        "provider": "evn",
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": True
    }
    assert config_entry.data == {}
    assert config_entry.options == {
        "name": "My Provider",
        "provider": "evn",
        "tariff_type": tariff_type,
        "clock_offset": clock_offset,
        "custom_day_price": custom_day_price,
        "custom_night_price": custom_night_price,
        "use_legacy_day_night_algorithm": True
    }
    assert config_entry.title == "My Provider"

    # Check config entry is reloaded with new options
    await hass.async_block_till_done()

    # Check the entities were updated, no new entities were created
    assert len(hass.states.async_all()) == 2

    state = hass.states.get("sensor.my_provider_price")
    assert state.attributes == {
        'friendly_name': 'My Provider Price',
        'icon': 'mdi:currency-eur',
        'state_class': SensorStateClass.MEASUREMENT,
        'unit_of_measurement': 'EUR/kWh'
    }

    state = hass.states.get("sensor.my_provider_tariff")
    assert state.attributes == {
        'friendly_name': 'My Provider Tariff',
        'icon': 'mdi:clock-time-ten',
    }
