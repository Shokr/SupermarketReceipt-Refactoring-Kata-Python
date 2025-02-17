### Unit Test Report: Coverage & Impact

Here’s a breakdown of the unit tests across the codebase and their effects on system reliability:

---

#### **1. `test_catalog.py` - Catalog Functionality**

**Key Tests**:

- `test_add_product_valid_price`: Ensures products are added to the catalog with valid prices.
- `test_add_product_non_positive_price`: Validates that negative/zero prices raise errors.
- `test_unit_price_returns_zero_for_missing_product`: Confirms missing products return a default price.

**Impact**:

- **Data Validation**: Guarantees price integrity in the catalog.
- **Edge Cases**: Prevents invalid pricing scenarios.

---

#### **2. `test_model_objects.py` - Domain Model Integrity**

**Key Tests**:

- `test_product_creation_valid`: Validates `Product` creation with correct fields.
- `test_product_empty_id_raises_error`: Ensures non-empty product IDs.
- `test_special_offer_calculations`: Verifies discount logic for `THREE_FOR_TWO`, `TWO_FOR_AMOUNT`, etc.
- `test_offer_validation`: Checks invalid offers/products/arguments raise errors.

**Impact**:

- **Business Logic**: Ensures offers calculate discounts accurately.
- **Immutable Rules**: Invalid objects (e.g., empty product names) cannot exist.

---

#### **3. `test_receipt.py` - Receipt Calculations**

**Key Tests**:

- `test_receipt_total_price`: Validates total price after discounts.
- `test_receipt_add_items_and_discounts`: Confirms items/discounts are stored correctly.

**Impact**:

- **Financial Accuracy**: Prevents miscalculations in receipts.
- **State Management**: Ensures items and discounts are tracked properly.

---

#### **4. `test_receipt_printer.py` - Receipt Formatting**

**Key Tests**:

- `test_receipt_printer_format`: Checks product names, quantities, and discounts appear in output.

**Impact**:

- **User Experience**: Guarantees readable receipts with aligned columns.
- **Edge Formatting**: Handles weight-based quantities (e.g., `0.500` kg).

---

#### **5. `test_shopping_cart.py` - Cart & Offers**

**Key Tests**:

- `test_add_item_quantity`: Validates cart updates product quantities.
- `test_handle_offers_applies_discount`: Ensures offers generate valid discounts.

**Impact**:

- **Offer Application**: Confirms discounts are applied only when eligible.
- **State Tracking**: Cart accurately tracks product quantities.

---

#### **6. `test_teller.py` - Checkout Workflow**

**Key Tests**:

- `test_teller_process_items`: Validates items are converted to receipt entries.

**Impact**:

- **End-to-End Workflow**: Ensures the checkout process integrates catalog, cart, and receipt.

---

### **Overall Impact**

- **Reliability**: Tests cover critical paths like pricing, discounts, and data validation.
- **Safety**: Immutable models + validation prevent invalid states.
- **Maintainability**: Clear test cases simplify future refactoring.

---
