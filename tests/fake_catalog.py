from catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    """An in-memory implementation of the catalog for testing purposes."""

    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product, price):
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product):
        return self.prices[product.name]
