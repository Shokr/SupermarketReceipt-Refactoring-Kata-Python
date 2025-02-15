import unittest
from decimal import Decimal

from catalog import SupermarketCatalog
from model_objects import Discount, Offer, Product, ProductQuantity, ProductUnit, SpecialOfferType
from receipt import Receipt, ReceiptItem
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller


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

    def test_default_quantity_is_zero(self):
        pq = ProductQuantity(self.product)
        self.assertEqual(pq.quantity, Decimal(
            '0'))  # Default is now Decimal('0') as per class definition, might want to change to Decimal('1') if that's more logical for default.

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


class TestReceiptPrinter(unittest.TestCase):

    def setUp(self):
        self.printer = ReceiptPrinter()
        self.product1 = Product("apple", "Apple", ProductUnit.EACH)
        self.product2 = Product("banana", "Banana", ProductUnit.KILO)

    def test_print_receipt_item_each(self):
        item = ReceiptItem(self.product1, Decimal('2'), Decimal('0.50'), Decimal('1.00'))
        expected_output = "Apple                          1.00\n  0.50 * 2\n"
        self.assertEqual(self.printer.print_receipt_item(item), expected_output)

    def test_print_receipt_item_kilo(self):
        item = ReceiptItem(self.product2, Decimal('0.5'), Decimal('2.00'), Decimal('1.00'))
        expected_output = "Banana                         1.00\n  2.00 * 0.500\n"
        self.assertEqual(self.printer.print_receipt_item(item), expected_output)

    def test_format_line_with_whitespace(self):
        line = self.printer.format_line_with_whitespace("Item Name", "1.00")
        expected_output_len = 40  # Default columns
        self.assertEqual(len(line.strip()), min(expected_output_len, len("Item Name") + len(
            "1.00")))  # Line length should be within column limit

    def test_print_price(self):
        self.assertEqual(self.printer.print_price(1.5), "1.50")
        self.assertEqual(self.printer.print_price(10), "10.00")
        self.assertEqual(self.printer.print_price(0.999), "1.00")  # check rounding

    def test_print_price_invalid_input(self):
        with self.assertRaisesRegex(ValueError, "Price must be a non-negative number."):
            self.printer.print_price(-1)
        with self.assertRaisesRegex(ValueError, "Price must be a non-negative number."):
            self.printer.print_price("invalid")  # type check - should be number

    def test_print_quantity_each(self):
        item = ReceiptItem(self.product1, Decimal('2'), Decimal('0.50'), Decimal('1.00'))
        self.assertEqual(self.printer.print_quantity(item), "2")

    def test_print_quantity_kilo(self):
        item = ReceiptItem(self.product2, Decimal('0.5'), Decimal('2.00'), Decimal('1.00'))
        self.assertEqual(self.printer.print_quantity(item), "0.500")

    def test_print_discount(self):
        discount = Discount(self.product1, "10% off apples", Decimal('0.10'))
        expected_output = "10% off apples (Apple)        0.10\n"
        self.assertEqual(self.printer.print_discount(discount), expected_output)

    def test_present_total(self):
        receipt = Receipt()
        receipt.total = Decimal('5.50')
        expected_output = "Total:                         5.50\n"
        self.assertEqual(self.printer.present_total(receipt), expected_output)

    def test_print_receipt_full(self):
        receipt = Receipt()
        receipt.add_product(self.product1, Decimal('2'), Decimal('0.50'), Decimal('1.00'))
        receipt.add_discount(Discount(self.product1, "10% off apples", Decimal('0.10')))
        receipt.total = Decimal('0.90')
        expected_receipt_output_lines = [
            "Apple                          1.00",
            "  0.50 * 2",
            "10% off apples (Apple)        0.10",
            "",
            "Total:                         0.90",
        ]
        actual_receipt_output = self.printer.print_receipt(receipt)
        actual_receipt_lines = [line.strip() for line in actual_receipt_output.strip().split(
            '\n')]  # split into lines and strip whitespace for comparison
        self.assertEqual(actual_receipt_lines, expected_receipt_output_lines)

    def test_receipt_printer_invalid_columns(self):
        with self.assertRaisesRegex(ValueError, "Columns must be a positive integer."):
            ReceiptPrinter(0)
        with self.assertRaisesRegex(ValueError, "Columns must be a positive integer."):
            ReceiptPrinter(-10)
        with self.assertRaisesRegex(ValueError, "Columns must be a positive integer."):
            ReceiptPrinter("invalid")  # type check - should be int


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.product1 = Product("apple", "Apple", ProductUnit.EACH)
        self.product2 = Product("banana", "Banana", ProductUnit.KILO)
        self.catalog_mock = unittest.mock.Mock(spec=SupermarketCatalog)  # Mock Catalog for price lookup

    def test_empty_cart_init(self):
        self.assertEqual(len(self.cart.items), 0)
        self.assertEqual(len(self.cart.product_quantities), 0)

    def test_add_item_quantity(self):
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.product_quantities[self.product1], Decimal('2.0'))
        self.assertEqual(self.cart.items[0].product, self.product1)
        self.assertEqual(self.cart.items[0].quantity, Decimal('2.0'))

    def test_add_item_single(self):
        self.cart.add_item(self.product1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.product_quantities[self.product1], Decimal('1.0'))
        self.assertEqual(self.cart.items[0].quantity, Decimal('1.0'))

    def test_add_multiple_items_same_product(self):
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.cart.add_item(self.product1)
        self.assertEqual(len(self.cart.items), 2)  # Items count reflects each addition
        self.assertEqual(self.cart.product_quantities[self.product1], Decimal('3.0'))  # Product Quantities aggregates

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

    def test_handle_offers_3_for_2_discount_applied(self):
        receipt = Receipt()
        offers = {self.product1: Offer(SpecialOfferType.THREE_FOR_TWO, self.product1, Decimal(0))}
        self.cart.add_item_quantity(self.product1, Decimal('3.0'))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "3 for 2")
        self.assertEqual(receipt.discounts[0].discount_amount, Decimal('-1.0'))

    def test_handle_offers_3_for_2_discount_not_applied_less_than_3(self):
        receipt = Receipt()
        offers = {self.product1: Offer(SpecialOfferType.THREE_FOR_TWO, self.product1, Decimal(0))}
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 0)

    def test_handle_offers_10_percent_discount(self):
        receipt = Receipt()
        offers = {self.product1: Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product1, Decimal('10.0'))}
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "10% off")
        self.assertEqual(receipt.discounts[0].discount_amount, Decimal('-0.20'))

    def test_handle_offers_2_for_amount_discount_applied(self):
        receipt = Receipt()
        offers = {self.product1: Offer(SpecialOfferType.TWO_FOR_AMOUNT, self.product1, Decimal('1.50'))}
        self.cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "2 for 1.50")
        self.assertEqual(receipt.discounts[0].discount_amount, Decimal('-0.50'))  # (2 * 1) - 1.50 = 0.50 discount

    def test_handle_offers_5_for_amount_discount_applied(self):
        receipt = Receipt()
        offers = {self.product1: Offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.product1, Decimal('3.00'))}
        self.cart.add_item_quantity(self.product1, Decimal('5.0'))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "5 for 3.00")
        self.assertEqual(receipt.discounts[0].discount_amount, Decimal('-2.00'))  # (5 * 1) - 3 = 2 discount

    def test_handle_offers_multiple_offers_different_products(self):
        receipt = Receipt()
        offers = {
            self.product1: Offer(SpecialOfferType.THREE_FOR_TWO, self.product1, Decimal(0)),
            self.product2: Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product2, Decimal('20.0'))
        }
        self.cart.add_item_quantity(self.product1, Decimal('3.0'))
        self.cart.add_item_quantity(self.product2, Decimal('1.0'))
        self.catalog_mock.unit_price.side_effect = [Decimal('1.0'),
                                                    Decimal('2.0')]  # Mock unit prices for product1 then product2
        self.cart.handle_offers(receipt, offers, self.catalog_mock)
        self.assertEqual(len(receipt.discounts), 2)
        discount_descriptions = set(d.description for d in receipt.discounts)
        self.assertEqual(discount_descriptions, {"3 for 2", "20% off"})  # Both discounts applied


class TestTeller(unittest.TestCase):

    def setUp(self):
        self.catalog_mock = unittest.mock.Mock(spec=SupermarketCatalog)
        self.teller = Teller(self.catalog_mock)
        self.product1 = Product("apple", "Apple", ProductUnit.EACH)
        self.product2 = Product("banana", "Banana", ProductUnit.KILO)

    def test_add_special_offer(self):
        offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product1, Decimal('10.0'))
        self.teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.product1, Decimal('10.0'))
        self.assertEqual(self.teller.offers[self.product1], offer)

    def test_add_special_offer_invalid_product(self):
        with self.assertRaisesRegex(ValueError, "Product cannot be None or empty."):
            self.teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, None, Decimal('10.0'))

    def test_add_special_offer_invalid_offer_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid offer type: InvalidOfferType"):
            self.teller.add_special_offer("InvalidOfferType", self.product1,
                                          Decimal('10.0'))  # Passing string instead of SpecialOfferType

    def test_checks_out_articles_from_empty_cart(self):
        cart = ShoppingCart()
        receipt = self.teller.checks_out_articles_from(cart)
        self.assertIsInstance(receipt, Receipt)
        self.assertEqual(len(receipt.items), 0)
        self.assertEqual(receipt.total_price(), Decimal('0.00'))

    def test_checks_out_articles_from_valid_cart_no_offers(self):
        cart = ShoppingCart()
        cart.add_item_quantity(self.product1, Decimal('2.0'))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        receipt = self.teller.checks_out_articles_from(cart)
        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(receipt.items[0].product, self.product1)
        self.assertEqual(receipt.items[0].quantity, Decimal('2.0'))
        self.assertEqual(receipt.items[0].total_price, Decimal('2.0'))
        self.assertEqual(receipt.total_price(), Decimal('2.00'))
        self.assertEqual(len(receipt.discounts), 0)

    def test_checks_out_articles_from_valid_cart_with_offers(self):
        cart = ShoppingCart()
        cart.add_item_quantity(self.product1, Decimal('3.0'))
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.product1, Decimal(0))
        self.catalog_mock.unit_price.return_value = Decimal('1.0')  # Mock unit price
        receipt = self.teller.checks_out_articles_from(cart)
        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(receipt.total_price(), Decimal('2.00'))  # 3 items at 1 each, 3 for 2 offer = 2 total
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].discount_amount, Decimal('-1.0'))

    def test_checks_out_articles_from_cart_invalid_quantity(self):
        cart = ShoppingCart()
        cart.add_item_quantity(self.product1, Decimal('-1.0'))
        with self.assertRaisesRegex(ValueError,
                                    "Invalid quantity \(-1.00\) for product: Product\(id='apple', name='Apple', unit=<ProductUnit.EACH: 1>\)"):
            self.teller.checks_out_articles_from(cart)

    def test_checks_out_articles_from_cart_unit_price_not_found(self):
        cart = ShoppingCart()
        cart.add_item(self.product1)
        self.catalog_mock.unit_price.return_value = None  # Mock no price found
        with self.assertRaisesRegex(ValueError,
                                    "Unit price not found for product: Product\(id='apple', name='Apple', unit=<ProductUnit.EACH: 1>\)"):
            self.teller.checks_out_articles_from(cart)

    def test_checks_out_articles_from_invalid_cart(self):
        with self.assertRaisesRegex(ValueError, "Cart cannot be None or empty."):
            self.teller.checks_out_articles_from(None)


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
