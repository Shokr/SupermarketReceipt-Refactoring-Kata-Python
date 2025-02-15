from decimal import Decimal

import pytest

from model_objects import (Discount, Offer, Product, ProductQuantity, ProductUnit, SpecialOfferType)


def test_product_creation_valid():
    product = Product("123", "Apple", ProductUnit.EACH)
    assert product.id == "123"
    assert product.name == "Apple"
    assert product.unit == ProductUnit.EACH


def test_product_empty_id_raises_error():
    with pytest.raises(ValueError):
        Product("", "Apple", ProductUnit.EACH)


def test_product_invalid_unit_raises_error():
    with pytest.raises(ValueError):
        Product("123", "Apple", "invalid_unit")  # type: ignore


def test_product_quantity_positive_validation():
    product = Product("123", "Apple", ProductUnit.EACH)
    ProductQuantity(product, Decimal("2.0"))  # No error


def test_product_quantity_zero_raises_error():
    product = Product("123", "Apple", ProductUnit.EACH)
    with pytest.raises(ValueError):
        ProductQuantity(product, Decimal("0"))


@pytest.mark.parametrize(
    "offer_type, quantity, unit_price, argument, expected_discount",
    [
        (SpecialOfferType.THREE_FOR_TWO, Decimal(3), Decimal(10), None, Decimal(10)),
        (SpecialOfferType.TWO_FOR_AMOUNT, Decimal(2), Decimal(5), Decimal(8), Decimal(2)),
        (SpecialOfferType.TEN_PERCENT_DISCOUNT, Decimal(2), Decimal(100), Decimal(10), Decimal(20)),
    ],
)
def test_special_offer_calculations(offer_type, quantity, unit_price, argument, expected_discount):
    discount = offer_type.calculate_discount(quantity, unit_price, argument)
    assert discount == expected_discount


def test_offer_validation():
    product = Product("123", "Apple", ProductUnit.EACH)
    with pytest.raises(ValueError):
        Offer("invalid_offer", product, Decimal(10))  # type: ignore
    with pytest.raises(ValueError):
        Offer(SpecialOfferType.THREE_FOR_TWO, "invalid_product", Decimal(10))  # type: ignore
    with pytest.raises(ValueError):
        Offer(SpecialOfferType.THREE_FOR_TWO, product, Decimal(-5))


def test_discount_validation():
    product = Product("123", "Apple", ProductUnit.EACH)
    with pytest.raises(ValueError):
        Discount("invalid_product", "Test", Decimal(10))  # type: ignore
    with pytest.raises(ValueError):
        Discount(product, "", Decimal(10))
    with pytest.raises(ValueError):
        Discount(product, "Test", Decimal(-5))
