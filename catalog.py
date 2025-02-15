from decimal import Decimal

from model_objects import Product


class SupermarketCatalog:
    def add_product(self, product: Product, price: Decimal):
        raise NotImplementedError

    def unit_price(self, product: Product) -> Decimal:
        raise NotImplementedError


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products: dict[Product, Decimal] = {}

    def add_product(self, product: Product, price: Decimal):
        if price <= Decimal(0):
            raise ValueError("Price must be positive")
        self.products[product] = price

    def unit_price(self, product: Product) -> Decimal:
        return self.products.get(product, Decimal(0))
