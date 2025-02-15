from decimal import Decimal
from typing import List

from model_objects import Discount, Product


class ReceiptItem:
    def __init__(self, product: Product, quantity: Decimal,
                 unit_price: Decimal, total_price: Decimal):
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items: List[ReceiptItem] = []
        self._discounts: List[Discount] = []

    def add_product(self, product: Product, quantity: Decimal,
                    unit_price: Decimal, total_price: Decimal):
        self._items.append(ReceiptItem(product, quantity, unit_price, total_price))

    def add_discount(self, discount: Discount):
        self._discounts.append(discount)

    def total_price(self) -> Decimal:
        items_total = sum(item.total_price for item in self._items)
        discounts_total = sum(discount.discount_amount for discount in self._discounts)
        return max(items_total + discounts_total, Decimal(0))
