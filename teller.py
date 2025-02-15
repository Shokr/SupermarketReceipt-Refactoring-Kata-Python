from decimal import Decimal
from typing import Dict

from model_objects import Offer, Product, SpecialOfferType
from receipt import Receipt


class Teller:
    def __init__(self, catalog):
        self.catalog = catalog
        self.offers: Dict[Product, Offer] = {}

    def add_special_offer(self, offer_type: SpecialOfferType,
                          product: Product, argument: Decimal):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, cart) -> Receipt:
        receipt = Receipt()

        for pq in cart.items:
            self._process_item(receipt, pq)

        cart.handle_offers(receipt, self.offers, self.catalog)
        return receipt

    def _process_item(self, receipt: Receipt, pq):
        product = pq.product
        quantity = pq.quantity
        unit_price = self.catalog.unit_price(product)

        if unit_price <= Decimal(0):
            raise ValueError(f"Invalid price for {product.name}")

        total_price = quantity * unit_price
        receipt.add_product(product, quantity, unit_price, total_price)
