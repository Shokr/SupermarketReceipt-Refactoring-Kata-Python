from decimal import Decimal

from model_objects import ProductUnit
from receipt import Receipt, ReceiptItem


class ReceiptPrinter:
    def __init__(self, columns=40):
        self.columns = columns

    def print_receipt(self, receipt: Receipt) -> str:
        lines = []
        for item in receipt.items:
            lines.append(self._format_item(item))
        for discount in receipt.discounts:
            lines.append(self._format_discount(discount))
        lines.append(self._format_total(receipt))
        return '\n'.join(lines)

    def _format_item(self, item: ReceiptItem) -> str:
        total = self._format_price(item.total_price)
        line = self._format_line(item.product.name, total)
        if item.quantity != Decimal(1):
            line += f"  {self._format_price(item.unit_price)} * {self._format_quantity(item)}\n"
        return line

    def _format_quantity(self, item: ReceiptItem) -> str:
        if item.product.unit == ProductUnit.EACH:
            return f"{item.quantity:.0f}"
        return f"{item.quantity:.3f}"

    def _format_price(self, price: Decimal) -> str:
        return f"${price:.2f}"

    def _format_line(self, name: str, price: str) -> str:
        return f"{name.ljust(self.columns - len(price))}{price}\n"
