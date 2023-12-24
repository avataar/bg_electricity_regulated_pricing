"""Constants for the bg_electricity_regulated_pricing integration."""
from homeassistant.const import UnitOfEnergy

DOMAIN = "bg_electricity_regulated_pricing"
BGN_PER_KILOWATT_HOUR = f"BGN/{UnitOfEnergy.KILO_WATT_HOUR}"

CONF_PROVIDER = "provider"
PROVIDERS = ["electrohold", "evn", "energo_pro", "custom"]

CONF_TARIFF_TYPE = "tariff_type"
TARIFF_TYPES = ["dual", "single"]

CONF_CLOCK_OFFSET = "clock_offset"

CONF_CUSTOM_DAY_PRICE = "custom_day_price"

CONF_CUSTOM_NIGHT_PRICE = "custom_night_price"

VAT_RATE = 0.2

PROVIDER_PRICES = {
    # Section 6.1, https://www.dker.bg/uploads/reshenia/2023/res_c_14_23.pdf
    "electrohold": {
        "day": .14875,
        "night": .05997,
        "fees": .01623 + .00754 + .04232
    },
    # Section 6.1, https://www.dker.bg/uploads/reshenia/2023/res_c_14_23.pdf
    "evn": {
        "day": .14667,
        "night": .05531,
        "fees": .01623 + .00803 + .04366
    },
    # Section 6.3, https://www.dker.bg/uploads/reshenia/2023/res_c_14_23.pdf
    "energo_pro": {
        "day": .15076,
        "night": .05279,
        "fees": .01623 + .00959 + .04825
    }
}
