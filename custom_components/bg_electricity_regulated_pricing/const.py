"""Constants for the bg_electricity_regulated_pricing integration."""
from homeassistant.const import UnitOfEnergy

DOMAIN = "bg_electricity_regulated_pricing"
EUR_PER_KILOWATT_HOUR = f"EUR/{UnitOfEnergy.KILO_WATT_HOUR}"

CONF_PROVIDER = "provider"
PROVIDERS = ["electrohold", "evn", "energo_pro", "custom"]

CONF_TARIFF_TYPE = "tariff_type"
TARIFF_TYPES = ["dual", "single"]

CONF_CLOCK_OFFSET = "clock_offset"

CONF_CUSTOM_DAY_PRICE = "custom_day_price"

CONF_CUSTOM_NIGHT_PRICE = "custom_night_price"

CONF_CLASSIC_DAY_NIGHT = "use_legacy_day_night_algorithm"

VAT_RATE = 0.2

PROVIDER_PRICES = {
    # Section III.1, III.2.1, https://www.dker.bg/uploads/reshenia/2026/res-c-13-2026.pdf
    # https://electrohold.bg/bg/sales/domakinstva/snabdyavane-po-regulirani-ceni/
    "electrohold": {
        "day": .09297,
        "night": .04103,
        "fees": .00018 + .00801 + .00347 + .02391
    },
    # Section III.1, III.2.2, https://www.dker.bg/uploads/reshenia/2026/res-c-13-2026.pdf
    # https://evn.bg/Home/Electricity.aspx
    "evn": {
        "day": .09297,
        "night": .04103,
        "fees": .00018 + .00801 + .00419 + .02347
    },
    # Section III.1, III.2.3, https://www.dker.bg/uploads/reshenia/2026/res-c-13-2026.pdf
    # https://www.energo-pro.bg/bitovi-klienti/ceni-tarifi
    "energo_pro": {
        "day": .09297,
        "night": .04103,
        "fees": .00018 + .00801 + .00499 + .02312
    }
}
