"""Test the bg_electricity_regulated_pricing integration."""
from datetime import datetime
from unittest import mock

import pytest
from homeassistant.components.sensor import SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bg_electricity_regulated_pricing.const import DOMAIN

# EUR
EXPECTED_PRICES = {
    "electrohold": {
        "day": 0.149736,
        "night": 0.088572
    },
    "evn": {
        "day": 0.149868,
        "night": 0.088704
    },
    "energo_pro": {
        "day": 0.151392,
        "night": 0.090228
    },
    "custom": {
        "day": 0.25,
        "night": 0.15
    }
}


@pytest.mark.parametrize("time, offset, tariff",
                         (
                                 ("2026-03-31 21:59 +03:00", 0, "day"),
                                 ("2026-03-31 22:00 +03:00", 0, "night"),
                                 ("2026-03-31 05:59 +03:00", 0, "night"),
                                 ("2026-03-31 06:00 +03:00", 0, "day"),
                                 ("2026-03-31 21:30 +03:00", 30, "night"),
                                 ("2026-03-31 05:30 +03:00", 30, "day"),
                                 ("2026-03-31 22:29 +03:00", -30, "day"),
                                 ("2026-03-31 06:29 +03:00", -30, "night"),
                                 ("2026-03-31 12:00 +03:00", 600, "night"),
                                 ("2026-03-31 20:00 +03:00", 600, "day"),
                                 ("2026-03-31 08:00 +03:00", -600, "night"),
                                 ("2026-03-31 16:00 +03:00", -600, "day")
                         ))
@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_winter(hass: HomeAssistant, provider: str, time: str, offset: int, tariff: str) -> None:
    """Test setting up and removing a config entry with current prices and default day/night algorithm in winter."""
    with mock_clock(time):
        await do_setup_test(hass, provider, "dual", tariff,
                            EXPECTED_PRICES, offset, False)
        await do_setup_test(hass, provider, "single", "day",
                            EXPECTED_PRICES, offset, False)


@pytest.mark.parametrize("time, offset, tariff",
                         (
                                 ("2026-04-01 22:59 +03:00", 0, "day"),
                                 ("2026-04-01 23:00 +03:00", 0, "night"),
                                 ("2026-04-01 06:59 +03:00", 0, "night"),
                                 ("2026-04-01 07:00 +03:00", 0, "day"),
                                 ("2026-04-01 22:30 +03:00", 30, "night"),
                                 ("2026-04-01 06:30 +03:00", 30, "day"),
                                 ("2026-04-01 23:29 +03:00", -30, "day"),
                                 ("2026-04-01 07:29 +03:00", -30, "night"),
                                 ("2026-04-01 13:00 +03:00", 600, "night"),
                                 ("2026-04-01 21:00 +03:00", 600, "day"),
                                 ("2026-04-01 09:00 +03:00", -600, "night"),
                                 ("2026-04-01 17:00 +03:00", -600, "day")
                         ))
@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_summer(hass: HomeAssistant, provider: str, time: str, offset: int, tariff: str) -> None:
    """Test setting up and removing a config entry with current prices and default day/night algorithm in summer."""
    with mock_clock(time):
        await do_setup_test(hass, provider, "dual", tariff,
                            EXPECTED_PRICES, offset, False)
        await do_setup_test(hass, provider, "single", "day",
                            EXPECTED_PRICES, offset, False)


@pytest.mark.parametrize("time, offset, tariff",
                         (
                                 ("2026-10-31 21:59 +02:00", 0, "day"),
                                 ("2026-10-31 22:00 +02:00", 0, "night"),
                                 ("2026-10-31 05:59 +02:00", 0, "night"),
                                 ("2026-10-31 06:00 +02:00", 0, "day"),
                                 ("2026-10-31 21:30 +02:00", 30, "night"),
                                 ("2026-10-31 05:30 +02:00", 30, "day"),
                                 ("2026-10-31 22:29 +02:00", -30, "day"),
                                 ("2026-10-31 06:29 +02:00", -30, "night"),
                                 ("2026-10-31 12:00 +02:00", 600, "night"),
                                 ("2026-10-31 20:00 +02:00", 600, "day"),
                                 ("2026-10-31 08:00 +02:00", -600, "night"),
                                 ("2026-10-31 16:00 +02:00", -600, "day")
                         ))
@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_winter_legacy(hass: HomeAssistant, provider: str, time: str, offset: int, tariff: str) -> None:
    """Test setting up and removing a config entry with current prices and legacy day/night algorithm in winter."""
    with mock_clock(time):
        await do_setup_test(hass, provider, "dual", tariff,
                            EXPECTED_PRICES, offset, True)
        await do_setup_test(hass, provider, "single", "day",
                            EXPECTED_PRICES, offset, True)


@pytest.mark.parametrize("time, offset, tariff",
                         (
                                 ("2026-03-31 22:59 +03:00", 0, "day"),
                                 ("2026-03-31 23:00 +03:00", 0, "night"),
                                 ("2026-03-31 06:59 +03:00", 0, "night"),
                                 ("2026-03-31 07:00 +03:00", 0, "day"),
                                 ("2026-03-31 22:30 +03:00", 30, "night"),
                                 ("2026-03-31 06:30 +03:00", 30, "day"),
                                 ("2026-03-31 23:29 +03:00", -30, "day"),
                                 ("2026-03-31 07:29 +03:00", -30, "night"),
                                 ("2026-03-31 13:00 +03:00", 600, "night"),
                                 ("2026-03-31 21:00 +03:00", 600, "day"),
                                 ("2026-03-31 09:00 +03:00", -600, "night"),
                                 ("2026-03-31 17:00 +03:00", -600, "day")
                         ))
@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_summer_legacy(hass: HomeAssistant, provider: str, time: str, offset: int, tariff: str) -> None:
    """Test setting up and removing a config entry with current prices and legacy day/night algorithm in summer."""
    with mock_clock(time):
        await do_setup_test(hass, provider, "dual", tariff,
                            EXPECTED_PRICES, offset, True)
        await do_setup_test(hass, provider, "single", "day",
                            EXPECTED_PRICES, offset, True)


async def do_setup_test(hass: HomeAssistant, provider: str, tariff_type: str,
                        expected_tariff: str, expected_prices, clock_offset, use_legacy_day_night_algorithm):
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
            "custom_night_price": custom_night_price,
            "use_legacy_day_night_algorithm": use_legacy_day_night_algorithm
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
    assert state.state == str(expected_prices[provider][expected_tariff])
    assert state.attributes == {
        'friendly_name': 'My Provider Price',
        'icon': 'mdi:currency-eur',
        'state_class': SensorStateClass.MEASUREMENT,
        'unit_of_measurement': 'EUR/kWh'
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


def mock_clock(time_string: str):
    return mock.patch(
        "custom_components.bg_electricity_regulated_pricing.sensor.now_bg",
        return_value=datetime.strptime(time_string, "%Y-%m-%d %H:%M %z"))
