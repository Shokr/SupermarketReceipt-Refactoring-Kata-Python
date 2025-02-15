from decimal import Decimal

from model_objects import Discount, Product, ProductUnit
from receipt import Receipt
from receipt_printer import ReceiptPrinter


def test_receipt_printer_format():
    product1 = Product("123", "Apple", ProductUnit.EACH)
    product2 = Product("456", "Banana", ProductUnit.KILO)

    receipt = Receipt()
    receipt.add_product(product1, Decimal(3), Decimal("2.00"), Decimal("6.00"))
    receipt.add_product(product2, Decimal("0.5"), Decimal("4.00"), Decimal("2.00"))
    receipt.add_discount(Discount(product1, "3 for 2", Decimal("2.00")))

    printer = ReceiptPrinter()
    output = printer.print_receipt(receipt)

    assert "Apple" in output
    assert "Banana" in output
    assert "0.500" in output
