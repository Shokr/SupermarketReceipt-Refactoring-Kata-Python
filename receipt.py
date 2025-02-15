class ReceiptItem:
    """
    Represents an item in a receipt.

    Attributes:
        product (str): The name of the product.
        quantity (int): The quantity of the product purchased.
        price (float): The unit price of the product.
        total_price (float): The total price for the quantity purchased.
    """

    def __init__(self, product: str, quantity: int, price: float, total_price: float):
        if not isinstance(product, str) or not product:
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(total_price, (int, float)) or total_price < 0:
            raise ValueError("Total price must be a non-negative number.")

        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Discount:
    """
    Represents a discount applied to a receipt.

    Attributes:
        description (str): A description of the discount.
        discount_amount (float): The amount of discount applied.
    """

    def __init__(self, description: str, discount_amount: float):
        if not isinstance(description, str) or not description:
            raise ValueError("Discount description must be a non-empty string.")
        if not isinstance(discount_amount, (int, float)) or discount_amount > 0:
            raise ValueError("Discount amount must be a negative number.")

        self.description = description
        self.discount_amount = discount_amount


class Receipt:
    """
    Represents a receipt containing purchased items and applied discounts.
    """

    def __init__(self):
        self._items = []
        self._discounts = []

    def total_price(self) -> float:
        """
        Calculates the total price of the receipt, including discounts.

        Returns:
            float: The final total amount after applying discounts.
        """
        total = sum(item.total_price for item in self._items)
        total += sum(discount.discount_amount for discount in self._discounts)
        return max(total, 0)  # Ensure the total doesn't go negative

    def add_product(self, product: str, quantity: int, price: float):
        """
        Adds a product to the receipt.

        Args:
            product (str): The name of the product.
            quantity (int): The quantity of the product purchased.
            price (float): The unit price of the product.
        """
        total_price = quantity * price
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, description: str, discount_amount: float):
        """
        Adds a discount to the receipt.

        Args:
            description (str): A description of the discount.
            discount_amount (float): The amount of discount applied.
        """
        self._discounts.append(Discount(description, discount_amount))

    @property
    def items(self):
        """
        Gets the list of items in the receipt.

        Returns:
            list[ReceiptItem]: A copy of the list of receipt items.
        """
        return self._items[:]

    @property
    def discounts(self):
        """
        Gets the list of discounts applied to the receipt.

        Returns:
            list[Discount]: A copy of the list of discounts.
        """
        return self._discounts[:]
