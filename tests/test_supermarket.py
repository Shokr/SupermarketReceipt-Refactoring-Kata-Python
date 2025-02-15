import unittest
from decimal import Decimal
from unittest import mock

from catalog import SupermarketCatalog
from model_objects import Discount, Offer, Product, ProductQuantity, ProductUnit, SpecialOfferType
from receipt import Receipt
from shopping_cart import ShoppingCart


class TestProduct(unittest.TestCase):

    def test_valid_product_creation(self):
        product = Product("1234", "Test Product", ProductUnit.EACH)
        self.assertEqual(product.id, "1234")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.unit, ProductUnit.EACH)

    def test_invalid_unit_type(self):
        with self.assertRaisesRegex(ValueError, "Unit must be a valid ProductUnit"):
            Product("1234", "Test Product", "InvalidUnit")  # Passing string instead of ProductUnit

    def test_empty_product_id(self):
        with self.assertRaisesRegex(ValueError, "Product ID cannot be empty"):
            Product("", "Test Product", ProductUnit.EACH)

    def test_empty_product_name(self):
        with self.assertRaisesRegex(ValueError, "Product name cannot be empty"):
            Product("1234", "", ProductUnit.EACH)

    def test_product_to_dict(self):
        product = Product("1234", "Test Product", ProductUnit.KILO)
        expected_dict = {'id': '1234', 'name': 'Test Product', 'unit': 2}  # KILO's value is 2 in Enum
        self.assertEqual(product.to_dict(), expected_dict)

    def test_product_from_dict(self):
        data = {'id': '5678', 'name': 'Dict Product', 'unit': 3}  # GRAM's value is 3 in Enum
        product = Product.from_dict(data)
        self.assertEqual(product.id, '5678')
        self.assertEqual(product.name, 'Dict Product')
        self.assertEqual(product.unit, ProductUnit.GRAM)

    def test_product_from_dict_missing_field(self):
        data = {'name': 'Missing ID Product', 'unit': 1}  # EACH's value is 1 in Enum
        with self.assertRaisesRegex(ValueError, "Missing required field: 'id'"):
            Product.from_dict(data)

    def test_product_from_dict_invalid_unit_value(self):
        data = {'id': '9012', 'name': 'Invalid Unit Product', 'unit': 99}  # 99 is not a valid ProductUnit
        with self.assertRaisesRegex(ValueError, "Invalid ProductUnit value: 99"):
            Product.from_dict(data)


class TestProductQuantity(unittest.TestCase):

    def setUp(self):
        self.product = Product("apple", "Apple", ProductUnit.EACH)

    def test_valid_product_quantity(self):
        pq = ProductQuantity(self.product, Decimal('2.5'))
        self.assertEqual(pq.product, self.product)
        self.assertEqual(pq.quantity, Decimal('2.5'))

    def test_invalid_quantity_zero(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be positive"):
            ProductQuantity(self.product, Decimal('0'))

    def test_invalid_quantity_negative(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be positive"):
            ProductQuantity(self.product, Decimal('-1'))


class TestOffer(unittest.TestCase):

    def setUp(self):
        self.product = Product("apple", "Apple", ProductUnit.EACH)

    def test_valid_offer_creation(self):
        offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product, Decimal('10.0'))
        self.assertEqual(offer.offer_type, SpecialOfferType.TEN_PERCENT_DISCOUNT)
        self.assertEqual(offer.product, self.product)
        self.assertEqual(offer.argument, Decimal('10.0'))

    def test_invalid_offer_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid offer type"):
            Offer("InvalidOfferType", self.product, Decimal('10.0'))  # Passing string instead of SpecialOfferType

    def test_invalid_product_reference(self):
        with self.assertRaisesRegex(ValueError, "Invalid product reference"):
            Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, "InvalidProduct",
                  Decimal('10.0'))  # Passing string instead of Product

    def test_invalid_discount_percentage_too_high(self):
        with self.assertRaisesRegex(ValueError, "Discount percentage must be between 0-100"):
            Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product, Decimal('100.0'))

    def test_invalid_discount_percentage_zero(self):
        with self.assertRaisesRegex(ValueError, "Discount percentage must be between 0-100"):
            Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product, Decimal('0'))

    def test_invalid_offer_amount_zero(self):
        for offer_type in [SpecialOfferType.TWO_FOR_AMOUNT, SpecialOfferType.FIVE_FOR_AMOUNT]:
            with self.assertRaisesRegex(ValueError, "Offer amount must be positive"):
                Offer(offer_type, self.product, Decimal('0'))

    def test_invalid_offer_amount_negative(self):
        for offer_type in [SpecialOfferType.TWO_FOR_AMOUNT, SpecialOfferType.FIVE_FOR_AMOUNT]:
            with self.assertRaisesRegex(ValueError, "Offer amount must be positive"):
                Offer(offer_type, self.product, Decimal('-10'))


class TestDiscount(unittest.TestCase):

    def setUp(self):
        self.product = Product("apple", "Apple", ProductUnit.EACH)

    def test_valid_discount_creation(self):
        discount = Discount(self.product, "10% off apples", Decimal('1.00'))
        self.assertEqual(discount.product, self.product)
        self.assertEqual(discount.description, "10% off apples")
        self.assertEqual(discount.discount_amount, Decimal('1.00'))

    def test_invalid_product_reference(self):
        with self.assertRaisesRegex(ValueError, "Invalid product reference"):
            Discount("InvalidProduct", "10% off", Decimal('1.00'))  # Passing string instead of Product

    def test_empty_discount_description(self):
        with self.assertRaisesRegex(ValueError, "Discount description required"):
            Discount(self.product, "", Decimal('1.00'))

    def test_invalid_discount_amount_zero(self):
        with self.assertRaisesRegex(ValueError, "Discount amount must be positive"):
            Discount(self.product, "Free item", Decimal('0'))

    def test_invalid_discount_amount_negative(self):
        with self.assertRaisesRegex(ValueError, "Discount amount must be positive"):
            Discount(self.product, "Negative discount", Decimal('-1.00'))


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.product1 = Product("apple", "Apple", ProductUnit.EACH)
        self.product2 = Product("banana", "Banana", ProductUnit.KILO)
        self.catalog_mock = mock.Mock(spec=SupermarketCatalog)  # Mock Catalog for price lookup

    def test_empty_cart_init(self):
        self.assertEqual(len(self.cart.items), 0)
        self.assertEqual(len(self.cart.product_quantities), 0)

    def test_add_item_quantity(self):
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.product_quantities[self.product1], Decimal('2.0'))
        self.assertEqual(self.cart.items[0].product, self.product1)
        self.assertEqual(self.cart.items[0].quantity, Decimal('2.0'))

    def test_add_item(self):
        self.cart.add_item(self.product1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.product_quantities[self.product1], Decimal('1.0'))
        self.assertEqual(self.cart.items[0].quantity, Decimal('1.0'))

    def test_add_item_quantity_invalid(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero."):
            self.cart.add_item_quantity(self.product1, Decimal('-1.0'))
        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero."):
            self.cart.add_item_quantity(self.product1, Decimal('0'))

    def test_handle_offers_no_offers(self):
        receipt = Receipt()
        offers = {}
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 0)


class TestSupermarketCatalog(unittest.TestCase):  # Basic placeholder tests for SupermarketCatalog as methods are stubs

    def setUp(self):
        self.catalog = SupermarketCatalog()
        self.product = Product("test_prod", "Test Product", ProductUnit.EACH)

    def test_add_product_placeholder(self):
        # As the method is a placeholder, we just check if it runs without error for now
        try:
            self.catalog.add_product(self.product, 1.0)
        except Exception as e:
            self.fail(f"add_product raised an exception: {e}")

    def test_unit_price_placeholder(self):
        # As the method is a placeholder, we just check if it runs without error and returns None (default behavior if not implemented)
        price = self.catalog.unit_price(self.product)
        self.assertIsNone(price)


if __name__ == '__main__':
    unittest.main()
