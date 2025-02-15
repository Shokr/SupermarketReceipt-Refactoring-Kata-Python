from decimal import Decimal

from catalog import FakeCatalog
from model_objects import Product, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller


def test_teller_process_items():
    catalog = FakeCatalog()
    product = Product("123", "Apple", ProductUnit.EACH)
    catalog.add_product(product, Decimal("5.00"))

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item(product)

    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt._items) == 1
    assert receipt.total_price() == Decimal("5.00")
