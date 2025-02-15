from model_objects import Discount, ProductQuantity, SpecialOfferType


class ShoppingCart:
    """
    A class representing a shopping cart that allows adding products with specified quantities
    and applies special offers during checkout.
    """

    def __init__(self):
        """Initializes an empty shopping cart."""
        self._items = []
        self._product_quantities = {}

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

    def add_item_quantity(self, product, quantity):
        """
        Adds a specified quantity of a product to the cart.

        :param product: The product to add.
        :param quantity: The quantity of the product.
        :raises ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self._items.append(ProductQuantity(product, quantity))
        self._product_quantities[product] = self._product_quantities.get(product, 0) + quantity

    def handle_offers(self, receipt, offers, catalog):
        """
        Applies available offers to the shopping cart and updates the receipt with discounts.

        :param receipt: The receipt object where discounts are recorded.
        :param offers: A dictionary of product offers.
        :param catalog: The catalog to retrieve product prices.
        """
        for product, quantity in self._product_quantities.items():
            if product not in offers:
                continue

            offer = offers[product]
            unit_price = catalog.unit_price(product)
            quantity_as_int = int(quantity)
            discount = None
            x = 1

            if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                x = 3
                if quantity_as_int >= 3:
                    number_of_x = quantity_as_int // x
                    discount_amount = number_of_x * unit_price
                    discount = Discount(product, "3 for 2", -discount_amount)

            elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                x = 2
                if quantity_as_int >= 2:
                    total = offer.argument * (quantity_as_int // x) + (quantity_as_int % 2 * unit_price)
                    discount_amount = unit_price * quantity - total
                    discount = Discount(product, f"2 for {offer.argument}", -discount_amount)

            elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                x = 5
                if quantity_as_int >= 5:
                    number_of_x = quantity_as_int // x
                    discount_total = unit_price * quantity - (
                            offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                    discount = Discount(product, f"{x} for {offer.argument}", -discount_total)

            elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                discount = Discount(product, f"{offer.argument}% off",
                                    -quantity * unit_price * offer.argument / 100.0)

            if discount:
                receipt.add_discount(discount)
