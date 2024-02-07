"""Sensor platform for bg_electricity_regulated_pricing integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, \
    SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import utcnow
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo


from .const import CONF_TARIFF_TYPE, CONF_PROVIDER, CONF_CUSTOM_DAY_PRICE, \
    CONF_CUSTOM_NIGHT_PRICE, PROVIDER_PRICES, CONF_CLOCK_OFFSET, \
    BGN_PER_KILOWATT_HOUR, VAT_RATE, DOMAIN


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize bg_electricity_regulated_pricing config entry."""
    name = config_entry.title
    unique_id = config_entry.entry_id

    tariff_type = config_entry.options[CONF_TARIFF_TYPE]
    clock_offset = config_entry.options[CONF_CLOCK_OFFSET]
    provider = config_entry.options[CONF_PROVIDER]
    if provider == "custom":
        price_day = config_entry.options[CONF_CUSTOM_DAY_PRICE]
        price_night = config_entry.options[CONF_CUSTOM_NIGHT_PRICE]
    else:
        price_day = (PROVIDER_PRICES[provider]["day"]
                     + PROVIDER_PRICES[provider]["fees"]) * (1 + VAT_RATE)
        price_night = (PROVIDER_PRICES[provider]["night"]
                       + PROVIDER_PRICES[provider]["fees"]) * (1 + VAT_RATE)

    price_provider = BgElectricityRegulatedPricingProvider(tariff_type, clock_offset,
                                                           price_day, price_night)

    desc_price = SensorEntityDescription(
        key="price",
        translation_key="price",
        icon="mdi:cash",
        native_unit_of_measurement=BGN_PER_KILOWATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=6,
        has_entity_name=True,
    )

    desc_tariff = SensorEntityDescription(
        key="tariff",
        translation_key="tariff",
        icon="mdi:clock-time-ten",
        has_entity_name=True,
    )

    async_add_entities([
        BgElectricityRegulatedPricingPriceSensorEntity(price_provider, unique_id,
                                                       name, desc_price),
        BgElectricityRegulatedPricingTariffSensorEntity(price_provider, unique_id,
                                                        name, desc_tariff)
    ])


def now_utc():
    return utcnow()


class BgElectricityRegulatedPricingSensorEntity(SensorEntity):
    """BgElectricityRegulatedPricing Sensor base."""

    def __init__(self, price_provider: BgElectricityRegulatedPricingProvider,
                 unique_id: str, name: str,
                 description: SensorEntityDescription) -> None:
        super().__init__()
        self.entity_description = description
        self._attr_unique_id = unique_id + "_" + description.key
        self._price_provider = price_provider
        self._device_name = name
        self._attr_device_info = DeviceInfo(
            name=name,
            identifiers={(DOMAIN, unique_id)},
            entry_type=DeviceEntryType.SERVICE,
        )


class BgElectricityRegulatedPricingPriceSensorEntity(
    BgElectricityRegulatedPricingSensorEntity
):
    """BgElectricityRegulatedPricing Sensor for price."""

    def __init__(self, price_provider: BgElectricityRegulatedPricingProvider,
                 unique_id: str, name: str,
                 description: SensorEntityDescription) -> None:
        super().__init__(price_provider, unique_id, name, description)
        self.update()

    def update(self) -> None:
        self._attr_native_value = self._price_provider.price()


class BgElectricityRegulatedPricingTariffSensorEntity(
    BgElectricityRegulatedPricingSensorEntity
):
    """BgElectricityRegulatedPricing Sensor for tariff."""

    def __init__(self, price_provider: BgElectricityRegulatedPricingProvider,
                 unique_id: str, name: str,
                 description: SensorEntityDescription) -> None:
        super().__init__(price_provider, unique_id, name, description)
        self.update()

    def update(self):
        self._attr_native_value = self._price_provider.tariff()


class BgElectricityRegulatedPricingProvider:
    """Pricing provider aware of current tariff and price."""

    def __init__(self, tariff_type, clock_offset, price_day, price_night):
        self._tariff_type = tariff_type
        self._clock_offset = clock_offset
        self._price_day = price_day
        self._price_night = price_night

    def tariff(self):
        # Current hour and minutes in minutes since midnight, UTC+2.
        # Night tariff starts at 22:00 and ends ot 06:00 UTC+2 (no summer time)
        utc = now_utc()
        hour_minutes = (
                               (utc.hour + 2) % 24 * 60
                               + utc.minute
                               + self._clock_offset
                       ) % 1440
        if self._tariff_type == "dual":
            if hour_minutes >= 22 * 60 or hour_minutes < 6 * 60:
                return "night"
        return "day"

    def price(self):
        if self.tariff() == "day":
            return self._price_day
        else:
            return self._price_night
