from decimal import Decimal

import pytest

from catalog import FakeCatalog
from model_objects import Product, ProductUnit


@pytest.fixture
def sample_product():
    return Product("123", "Test Product", ProductUnit.EACH)


def test_add_product_valid_price(sample_product):
    catalog = FakeCatalog()
    catalog.add_product(sample_product, Decimal("10.50"))
    assert catalog.unit_price(sample_product) == Decimal("10.50")


def test_add_product_non_positive_price(sample_product):
    catalog = FakeCatalog()
    with pytest.raises(ValueError):
        catalog.add_product(sample_product, Decimal("-5.00"))
    with pytest.raises(ValueError):
        catalog.add_product(sample_product, Decimal("0.00"))


def test_unit_price_returns_zero_for_missing_product(sample_product):
    catalog = FakeCatalog()
    assert catalog.unit_price(sample_product) == Decimal("0")
