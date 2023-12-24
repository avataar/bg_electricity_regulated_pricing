"""Common fixtures for the bg_electricity_regulated_pricing tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, patch
from typing import Any

import pytest
from pytest_homeassistant_custom_component.plugins import (
    enable_custom_integrations,
)


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Override async_setup_entry."""
    with patch(
            "custom_components.bg_electricity_regulated_pricing.async_setup_entry",
            return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(autouse=True)
def bg_electricity_regulated_pricing_fixture(enable_custom_integrations: Any) -> None:
    """Automatically use custom integrations."""
