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

PROVIDER_PRICES_BEFORE_JULY_2024 = {
    # Section 6.1, https://www.dker.bg/uploads/reshenia/2023/res_c_14_23.pdf
    "electrohold": {
        "day": .14875,
        "night": .05997,
        "fees": .01623 + .00754 + .04232
    },
    # Section 6.2, https://www.dker.bg/uploads/reshenia/2023/res_c_14_23.pdf
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

PROVIDER_PRICES = {
    # Section 6.1, https://www.dker.bg/uploads/reshenia/2024/res-c-17-2024.pdf
    "electrohold": {
        "day": .16210,
        "night": .07104,
        "fees": .01354 + .00770 + .03803
    },
    # Section 6.2, https://www.dker.bg/uploads/reshenia/2024/res-c-17-2024.pdf
    "evn": {
        "day": .15926,
        "night": .06833,
        "fees": .01354 + .00819 + .03704
    },
    # Section 6.3, https://www.dker.bg/uploads/reshenia/2024/res-c-17-2024.pdf
    "energo_pro": {
        "day": .16341,
        "night": .06636,
        "fees": .01354 + .00977 + .03689
    }
}

PROVIDER_PRICES_BY_DATE = [
    {
        "until": 1719777600,  # midnight 2024-07-01 UTC+2
        "prices": PROVIDER_PRICES_BEFORE_JULY_2024
    },
    {
        "prices": PROVIDER_PRICES
    }
]
