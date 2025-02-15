from model_objects import ProductUnit


class ReceiptPrinter:
    """
    Handles the printing of a receipt in a formatted manner.
    """

    def __init__(self, columns: int = 40):
        """
        Initializes the ReceiptPrinter with a specified column width.

        Args:
            columns (int): The width of the printed receipt.
        """
        if not isinstance(columns, int) or columns <= 0:
            raise ValueError("Columns must be a positive integer.")
        self.columns = columns

    def print_receipt(self, receipt) -> str:
        """
        Generates a formatted receipt string.

        Args:
            receipt (Receipt): The receipt object to be printed.

        Returns:
            str: The formatted receipt output.
        """
        result = ""
        for item in receipt.items:
            result += self.print_receipt_item(item)

        for discount in receipt.discounts:
            result += self.print_discount(discount)

        result += "\n"
        result += self.present_total(receipt)
        return result

    def print_receipt_item(self, item) -> str:
        """
        Formats a receipt item as a string.

        Args:
            item (ReceiptItem): The item to be printed.

        Returns:
            str: The formatted receipt item.
        """
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)

        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"

        return line

    def format_line_with_whitespace(self, name: str, value: str) -> str:
        """
        Formats a line by aligning the name and value with whitespace.

        Args:
            name (str): The name or label.
            value (str): The value to be aligned.

        Returns:
            str: The formatted line.
        """
        whitespace_size = self.columns - len(name) - len(value)
        line = name + " " * max(whitespace_size, 1) + value + "\n"
        return line

    def print_price(self, price: float) -> str:
        """
        Formats the price to two decimal places.

        Args:
            price (float): The price value.

        Returns:
            str: The formatted price string.
        """
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        return "%.2f" % price

    def print_quantity(self, item) -> str:
        """
        Formats the quantity based on the unit type.

        Args:
            item (ReceiptItem): The item whose quantity needs formatting.

        Returns:
            str: The formatted quantity string.
        """
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return "%.3f" % item.quantity

    def print_discount(self, discount) -> str:
        """
        Formats a discount line for the receipt.

        Args:
            discount (Discount): The discount to be printed.

        Returns:
            str: The formatted discount line.
        """
        name = f"{discount.description} ({discount.product.name})"
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt) -> str:
        """
        Formats the total amount line for the receipt.

        Args:
            receipt (Receipt): The receipt object.

        Returns:
            str: The formatted total amount line.
        """
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
