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

EXPECTED_PRICES_BEFORE_JULY_2024 = {
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

EXPECTED_PRICES_BEFORE_JANUARY_2025 = {
    "electrohold": {
        "day": 0.265656,
        "night": 0.156384
    },
    "evn": {
        "day": 0.261648,
        "night": 0.152532
    },
    "energo_pro": {
        "day": 0.268344,
        "night": 0.151884
    },
    "custom": {
        "day": 0.25,
        "night": 0.15
    }
}

EXPECTED_PRICES = {
    "electrohold": {
        "day": 0.287856,
        "night": 0.169464
    },
    "evn": {
        "day": 0.283596,
        "night": 0.16536
    },
    "energo_pro": {
        "day": 0.291228,
        "night": 0.16506
    },
    "custom": {
        "day": 0.25,
        "night": 0.15
    }
}

EXPECTED_PRICES_BY_DATE = [
    {
        "until": 1719777600,  # midnight 2024-07-01 UTC+2
        "prices": EXPECTED_PRICES_BEFORE_JULY_2024
    },
    {
        "until": 1735682400,  # midnight 2025-01-01 UTC+2
        "prices": EXPECTED_PRICES_BEFORE_JANUARY_2025
    },
    {
        "prices": EXPECTED_PRICES
    }
]


@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_before_july_2024(hass: HomeAssistant, provider: str) -> None:
    """Test setting up and removing a config entry before July 2024."""
    await do_setup_test_with_mock(hass, provider, mock_time_before_july_2024,
                                  EXPECTED_PRICES_BEFORE_JULY_2024)


@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_before_january_2025(hass: HomeAssistant, provider: str) -> None:
    """Test setting up and removing a config entry before January 2025."""
    await do_setup_test_with_mock(hass, provider, mock_time_before_january_2025,
                                  EXPECTED_PRICES_BEFORE_JANUARY_2025)


@pytest.mark.parametrize("provider", ("electrohold", "evn", "energo_pro", "custom"))
async def test_prices_current(hass: HomeAssistant, provider: str) -> None:
    """Test setting up and removing a config entry with current prices."""
    await do_setup_test_with_mock(hass, provider, mock_time,
                                  EXPECTED_PRICES)


async def do_setup_test_with_mock(hass: HomeAssistant,
                                  provider: str, mock, expected_prices) -> None:
    with mock(21, 59):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices)

    with mock(22, 0):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices)

    with mock(5, 59):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices)

    with mock(6, 0):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices)

    # Meter clock is 30 minutes ahead
    with mock(21, 30):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices, 30)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, 30)

    with mock(5, 30):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices, 30)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, 30)

    # Meter clock is 30 minutes behind
    with mock(22, 29):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices, -30)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, -30)

    with mock(6, 29):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices, -30)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, -30)

    # Meter clock is 10 hours ahead
    with mock(12, 0):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices, 600)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, 600)

    with mock(20, 0):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices, 600)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, 600)

    # Meter clock is 10 hours behind
    with mock(8, 0):
        await do_setup_test(hass, provider, "dual", "night",
                            expected_prices, -600)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, -600)

    with mock(16, 0):
        await do_setup_test(hass, provider, "dual", "day",
                            expected_prices, -600)
        await do_setup_test(hass, provider, "single", "day",
                            expected_prices, -600)


async def do_setup_test(hass: HomeAssistant, provider: str, tariff_type: str,
                        expected_tariff: str, expected_prices, clock_offset=0):
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
    assert state.state == str(expected_prices[provider][expected_tariff])
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


def mock_time_before_july_2024(hour: int, minute: int):
    hour -= 2
    if hour < 0:
        hour += 24
    return mock.patch(
        "custom_components.bg_electricity_regulated_pricing.sensor.now_utc",
        return_value=datetime(2023, 12, 23, hour, minute, 0, 0, pytz.UTC))


def mock_time_before_january_2025(hour: int, minute: int):
    hour -= 2
    if hour < 0:
        hour += 24
    return mock.patch(
        "custom_components.bg_electricity_regulated_pricing.sensor.now_utc",
        return_value=datetime(2024, 12, 30, hour, minute, 0, 0, pytz.UTC))


def mock_time(hour: int, minute: int):
    hour -= 2
    if hour < 0:
        hour += 24
    return mock.patch(
        "custom_components.bg_electricity_regulated_pricing.sensor.now_utc",
        return_value=datetime(2025, 1, 1, hour, minute, 0, 0, pytz.UTC))
