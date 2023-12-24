"""Test the bg_electricity_regulated_pricing integration."""
from datetime import datetime
from unittest import mock

import pytest
import pytz
from homeassistant.components.sensor import SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bg_electricity_regulated_pricing.const import DOMAIN

EXPECTED_PRICES = {
    "electrohold": {
        "day": 0.257808,
        "night": 0.151272
    },
    "evn": {
        "day": 0.257508,
        "night": 0.147876
    },
    "energo_pro": {
        "day": 0.269796,
        "night": 0.152232
    },
    "custom": {
        "day": 0.25,
        "night": 0.15
    }
}


@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_setup_and_remove_config_entry(hass: HomeAssistant,
                                             provider: str) -> None:
    """Test setting up and removing a config entry."""
    with mock_time(21, 59):
        await do_setup_test(hass, provider, "dual", "day")
        await do_setup_test(hass, provider, "single", "day")

    with mock_time(22, 0):
        await do_setup_test(hass, provider, "dual", "night")
        await do_setup_test(hass, provider, "single", "day")

    with mock_time(5, 59):
        await do_setup_test(hass, provider, "dual", "night")
        await do_setup_test(hass, provider, "single", "day")

    with mock_time(6, 0):
        await do_setup_test(hass, provider, "dual", "day")
        await do_setup_test(hass, provider, "single", "day")

    # Meter clock is 30 minutes ahead
    with mock_time(21, 30):
        await do_setup_test(hass, provider, "dual", "night", 30)
        await do_setup_test(hass, provider, "single", "day", 30)

    with mock_time(5, 30):
        await do_setup_test(hass, provider, "dual", "day", 30)
        await do_setup_test(hass, provider, "single", "day", 30)

    # Meter clock is 30 minutes behind
    with mock_time(22, 29):
        await do_setup_test(hass, provider, "dual", "day", -30)
        await do_setup_test(hass, provider, "single", "day", -30)

    with mock_time(6, 29):
        await do_setup_test(hass, provider, "dual", "night", -30)
        await do_setup_test(hass, provider, "single", "day", -30)

    # Meter clock is 10 hours ahead
    with mock_time(12, 0):
        await do_setup_test(hass, provider, "dual", "night", 600)
        await do_setup_test(hass, provider, "single", "day", 600)

    with mock_time(20, 0):
        await do_setup_test(hass, provider, "dual", "day", 600)
        await do_setup_test(hass, provider, "single", "day", 600)

    # Meter clock is 10 hours behind
    with mock_time(8, 0):
        await do_setup_test(hass, provider, "dual", "night", -600)
        await do_setup_test(hass, provider, "single", "day", -600)

    with mock_time(16, 0):
        await do_setup_test(hass, provider, "dual", "day", -600)
        await do_setup_test(hass, provider, "single", "day", -600)


async def do_setup_test(hass: HomeAssistant, provider: str, tariff_type: str,
                        expected_tariff: str, clock_offset=0):
    registry = er.async_get(hass)
    custom_day_price = 0.25
    custom_night_price = 0.15

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

    price_entity_id = "sensor.my_provider_price"
    tariff_entity_id = "sensor.my_provider_tariff"

    # Check the price entity is registered in the entity registry
    assert registry.async_get(price_entity_id) is not None

    # Check the platform for price is setup correctly
    state = hass.states.get(price_entity_id)
    assert state.state == str(EXPECTED_PRICES[provider][expected_tariff])
    assert state.attributes == {
        'friendly_name': 'My Provider Price',
        'icon': 'mdi:currency-eur',
        'state_class': SensorStateClass.MEASUREMENT,
        'unit_of_measurement': 'BGN/kWh'
    }

    # Check the price entity is registered in the entity registry
    assert registry.async_get(tariff_entity_id) is not None

    # Check the platform for price is setup correctly
    state = hass.states.get(tariff_entity_id)
    assert state.state == expected_tariff
    assert state.attributes == {
        'friendly_name': 'My Provider Tariff',
        'icon': 'mdi:clock-time-ten'
    }

    # Remove the config entry
    assert await hass.config_entries.async_remove(config_entry.entry_id)
    await hass.async_block_till_done()

    # Check the state and entity registry entries are removed
    assert hass.states.get(price_entity_id) is None
    assert registry.async_get(price_entity_id) is None
    assert hass.states.get(tariff_entity_id) is None
    assert registry.async_get(tariff_entity_id) is None


def mock_time(hour: int, minute: int):
    hour -= 2
    if hour < 0:
        hour += 24
    return mock.patch(
        "custom_components.bg_electricity_regulated_pricing.sensor.now_utc",
        return_value=datetime(2023, 12, 23, hour, minute, 0, 0, pytz.UTC))
