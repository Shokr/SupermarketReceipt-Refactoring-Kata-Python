from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto
from typing import Any, Dict


class ProductUnit(Enum):
    """
    Represents the unit of measurement for a product.

    Attributes:
        EACH: Item is sold individually.
        KILO: Item is sold by kilograms.
        GRAM: Item is sold by grams.
        LITER: Item is sold by liters.
    """
    EACH = auto()
    KILO = auto()
    GRAM = auto()
    LITER = auto()

    @property
    def is_weight_based(self) -> bool:
        """Determines if the unit is weight-based (kilo or gram)."""
        return self in [ProductUnit.KILO, ProductUnit.GRAM]


@dataclass(frozen=True)
class Product:
    """
    Immutable value object representing a supermarket product.

    Attributes:
        id: Unique product identifier (non-empty string)
        name: Product name (non-empty string)
        unit: Measurement unit from ProductUnit enum
    """
    id: str
    name: str
    unit: ProductUnit

    def __post_init__(self) -> None:
        """Validates initialization values."""
        if not isinstance(self.unit, ProductUnit):
            raise ValueError("Unit must be a valid ProductUnit")
        if not self.id.strip():
            raise ValueError("Product ID cannot be empty")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes product to dictionary format."""
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit.value
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Creates Product from dictionary data."""
        try:
            return cls(
                id=str(data['id']),
                name=str(data['name']),
                unit=ProductUnit(data['unit'])
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid ProductUnit value: {data['unit']}") from e


@dataclass(frozen=True)
class ProductQuantity:
    """
    Represents a quantified product in a transaction.

    Attributes:
        product: Product reference
        quantity: Positive quantity in specified units
    """
    product: Product
    quantity: Decimal = field(default_factory=Decimal)

    def __post_init__(self) -> None:
        """Validates quantity is positive."""
        if self.quantity <= Decimal(0):
            raise ValueError("Quantity must be positive")


class SpecialOfferType(Enum):
    """
    Represents types of special offers available.

    Attributes:
        THREE_FOR_TWO: Buy 3 items, pay for 2
        TEN_PERCENT_DISCOUNT: Percentage discount on item
        TWO_FOR_AMOUNT: Buy 2 items for fixed price
        FIVE_FOR_AMOUNT: Buy 5 items for fixed price
    """
    THREE_FOR_TWO = ("3 for 2", "Buy 3 items, pay for 2")
    TEN_PERCENT_DISCOUNT = ("10% off", "Get 10% discount")
    TWO_FOR_AMOUNT = ("2 for {amount}", "Buy 2 items for a fixed price")
    FIVE_FOR_AMOUNT = ("5 for {amount}", "Buy 5 items for a fixed price")

    def __init__(self, display_text: str, description: str):
        self.display_text = display_text
        self.description = description

    def calculate_discount(self, quantity: Decimal, unit_price: Decimal, argument: Decimal) -> Decimal:
        if self == SpecialOfferType.THREE_FOR_TWO:
            return self._three_for_two(quantity, unit_price)
        elif self == SpecialOfferType.TWO_FOR_AMOUNT:
            return self._two_for_amount(quantity, unit_price, argument)
        elif self == SpecialOfferType.FIVE_FOR_AMOUNT:
            return self._five_for_amount(quantity, unit_price, argument)
        elif self == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            return self._percentage_discount(quantity, unit_price, argument)
        return Decimal(0)

    def _three_for_two(self, quantity: Decimal, unit_price: Decimal) -> Decimal:
        groups_of_three = quantity // Decimal(3)
        return groups_of_three * unit_price

    def _two_for_amount(self, quantity: Decimal, unit_price: Decimal, argument: Decimal) -> Decimal:
        if quantity >= Decimal(2):
            total = (quantity // Decimal(2)) * argument + (quantity % Decimal(2)) * unit_price
            return quantity * unit_price - total
        return Decimal(0)

    def _five_for_amount(self, quantity: Decimal, unit_price: Decimal, argument: Decimal) -> Decimal:
        if quantity >= Decimal(5):
            groups_of_five = quantity // Decimal(5)
            remaining_items = quantity % Decimal(5)
            discounted_total = (groups_of_five * argument) + (remaining_items * unit_price)
            return (quantity * unit_price) - discounted_total
        return Decimal(0)

    def _percentage_discount(self, quantity: Decimal, unit_price: Decimal, argument: Decimal) -> Decimal:
        return (quantity * unit_price * argument) / Decimal(100)


@dataclass(frozen=True)
class Offer:
    """
    Represents a pricing offer applicable to specific products.

    Attributes:
        offer_type: Type of special offer
        product: Product this offer applies to
        argument: Offer-specific parameter (percentage, fixed price, etc)
    """
    offer_type: SpecialOfferType
    product: Product
    argument: Decimal

    def __post_init__(self):
        if not isinstance(self.offer_type, SpecialOfferType):
            raise ValueError("Invalid offer type")
        if not isinstance(self.product, Product):
            raise ValueError("Invalid product")
        if self.argument <= Decimal(0):
            raise ValueError("Offer argument must be positive")



@dataclass(frozen=True)
class Discount:
    """
    Represents a calculated discount to be applied.

    Attributes:
        product: Product the discount applies to
        description: Human-readable discount description
        discount_amount: Monetary value of discount (positive)
    """
    product: Product
    description: str
    discount_amount: Decimal = field(default_factory=Decimal)

    def __post_init__(self) -> None:
        """Validates discount values."""
        if not isinstance(self.product, Product):
            raise ValueError("Invalid product reference")
        if not self.description.strip():
            raise ValueError("Discount description required")
        if self.discount_amount <= Decimal(0):
            raise ValueError("Discount amount must be positive")
