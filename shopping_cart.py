from decimal import Decimal
from typing import List

from model_objects import Discount, Product, ProductQuantity


class ShoppingCart:
    """
    A class representing a shopping cart that allows adding products with specified quantities
    and applies special offers during checkout.
    """

    def __init__(self):
        """Initializes an empty shopping cart."""
        self._items: List[ProductQuantity] = []
        self._product_quantities: dict[Product, Decimal] = {}

    @property
    def items(self):
        """Returns the list of items in the cart."""
        return self._items

    @property
    def product_quantities(self):
        """Returns a dictionary of product quantities in the cart."""
        return self._product_quantities

    def add_item(self, product):
        """
        Adds a single unit of the given product to the cart.

        :param product: The product to add.
        """
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: Decimal):
        if quantity <= Decimal(0):
            raise ValueError("Quantity must be positive")
        self._items.append(ProductQuantity(product, quantity))
        self._product_quantities[product] = self._product_quantities.get(product, Decimal(0)) + quantity

    def handle_offers(self, receipt, offers, catalog):
        for product, quantity in self._product_quantities.items():
            if offer := offers.get(product):
                unit_price = catalog.unit_price(product)
                discount_amount = offer.offer_type.calculate_discount(
                    quantity, unit_price, offer.argument
                )
                if discount_amount > Decimal(0):
                    receipt.add_discount(Discount(
                        product=product,
                        description=offer.offer_type.description,
                        discount_amount=-discount_amount
                    ))
