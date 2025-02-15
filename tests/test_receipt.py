from decimal import Decimal

from model_objects import Discount, Product, ProductUnit
from receipt import Receipt


def test_receipt_total_price():
    receipt = Receipt()
    product = Product("123", "Apple", ProductUnit.EACH)

    receipt.add_product(product, Decimal(2), Decimal("5.00"), Decimal("10.00"))
    receipt.add_discount(Discount(product, "Test Discount", Decimal("2.00")))  # Positive

    assert receipt.total_price() == Decimal("8.00")  # 10 - 2 = 8


def test_receipt_add_items_and_discounts():
    receipt = Receipt()
    product = Product("123", "Apple", ProductUnit.EACH)

    receipt.add_product(product, Decimal(1), Decimal("3.00"), Decimal("3.00"))
    receipt.add_discount(Discount(product, "Discount", Decimal("1.50")))

    assert len(receipt._items) == 1
    assert len(receipt._discounts) == 1
