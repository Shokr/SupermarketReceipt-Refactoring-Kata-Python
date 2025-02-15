from model_objects import Offer
from receipt import Receipt


class Teller:
    """
    The Teller class is responsible for processing purchases by checking out cart items,
    applying special offers, and generating a receipt.
    """

    def __init__(self, catalog):
        """
        Initializes the Teller with a product catalog and an empty dictionary of offers.

        :param catalog: An object that provides unit prices for products.
        """
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        """
        Adds a special offer for a given product.

        :param offer_type: The type of the special offer.
        :param product: The product to which the offer applies.
        :param argument: The argument related to the offer (e.g., discount percentage, quantity threshold).
        """
        if not product:
            raise ValueError("Product cannot be None or empty.")

        if offer_type not in Offer.VALID_OFFER_TYPES:  # Assuming Offer has predefined valid types
            raise ValueError(f"Invalid offer type: {offer_type}")

        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        """
        Processes the cart, computes the total price, applies any special offers,
        and generates a receipt.

        :param the_cart: The shopping cart containing product items and quantities.
        :return: A Receipt object containing the purchased products and total amount.
        """
        if not the_cart:
            raise ValueError("Cart cannot be None or empty.")

        receipt = Receipt()

        for pq in the_cart.items:
            p = pq.product
            quantity = pq.quantity

            if quantity <= 0:
                raise ValueError(f"Invalid quantity ({quantity}) for product: {p}")

            unit_price = self.catalog.unit_price(p)
            if unit_price is None:
                raise ValueError(f"Unit price not found for product: {p}")

            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        # Apply offers, if any
        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
