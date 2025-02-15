from decimal import Decimal

from catalog import FakeCatalog
from model_objects import Offer, Product, ProductUnit, SpecialOfferType
from receipt import Receipt
from shopping_cart import ShoppingCart


def test_add_item_quantity():
    cart = ShoppingCart()
    product = Product("123", "Apple", ProductUnit.EACH)

    cart.add_item_quantity(product, Decimal(2))
    assert cart.product_quantities[product] == Decimal(2)


def test_handle_offers_applies_discount():
    cart = ShoppingCart()
    product = Product("123", "Apple", ProductUnit.EACH)
    catalog = FakeCatalog()
    catalog.add_product(product, Decimal("10.00"))

    cart.add_item_quantity(product, Decimal(3))
    receipt = Receipt()
    offers = {product: Offer(SpecialOfferType.THREE_FOR_TWO, product, Decimal("1"))}

    cart.handle_offers(receipt, offers, catalog)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].discount_amount == Decimal("10.00")  # Positive
