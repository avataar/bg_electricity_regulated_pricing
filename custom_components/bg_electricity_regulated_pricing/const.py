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

# Prices converted from BGN, where the price per MWh was converted to EUR and rounded
# according to the law for introducing the EUR.
PROVIDER_PRICES = {
    # Section II.1, II.2, III.1, https://www.dker.bg/uploads/reshenia/2025/res-c-25-2025.pdf
    # https://electrohold.bg/bg/sales/domakinstva/snabdyavane-po-regulirani-ceni/
    "electrohold": {
        "day": .08955,
        "night": .03858,
        "fees": .00018 + .0076 + .00371 + .02374
    },
    # Section II.1, II.3, III.1, https://www.dker.bg/uploads/reshenia/2025/res-c-25-2025.pdf
    # https://evn.bg/Home/Electricity.aspx
    "evn": {
        "day": .08955,
        "night": .03858,
        "fees": .00018 + .0076 + .00419 + .02337
    },
    # Section II.1, II.4, III.1, https://www.dker.bg/uploads/reshenia/2025/res-c-25-2025.pdf
    # https://www.energo-pro.bg/bitovi-klienti/ceni-tarifi
    "energo_pro": {
        "day": .08955,
        "night": .03858,
        "fees": .00018 + .0076 + .005 + .02383
    }
}
