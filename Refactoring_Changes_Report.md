### Refactoring Changes Report

Here's a detailed breakdown of the key refactoring changes and their impact on the codebase:

---

#### **1. Data Modeling & Validation**

- **Changes**:
    - Introduced **immutable dataclasses** (`Product`, `ProductQuantity`, `Offer`, `Discount`) with `frozen=True`.
    - Added `__post_init__` validation for all value objects (e.g., non-empty `Product.name`, positive
      `Discount.discount_amount`).
    - Enhanced `ProductUnit` with `is_weight_based` property and expanded enum variants (e.g., `GRAM`, `LITER`).

- **Impact**:
    - **Data Integrity**: Invalid states (e.g., negative prices, empty product names) are now impossible to represent.
    - **Self-Documentation**: Clear structure via dataclasses reduces ambiguity.
    - **Safer Concurrency**: Immutability prevents accidental state changes.

---

#### **2. Special Offer Logic Centralization**

- **Changes**:
    - Moved discount calculation logic into `SpecialOfferType` methods (e.g., `calculate_discount`).
    - Removed conditional spaghetti in `ShoppingCart.handle_offers` in favor of polymorphic enum behavior.

- **Impact**:
    - **Single Responsibility**: Each offer type encapsulates its own logic.
    - **Extensibility**: Adding new offers (e.g., `BUY_ONE_GET_ONE`) requires minimal changes.
    - **Readability**: Simplified `handle_offers` with a clean delegation pattern.

---

#### **3. Precision & Type Safety**

- **Changes**:
    - Replaced `float` with `Decimal` for all monetary values and quantities.
    - Added **type hints** across all methods and classes.

- **Impact**:
    - **Accuracy**: Eliminates floating-point rounding errors in financial calculations.
    - **Static Analysis**: Tools like `mypy` can catch type mismatches early.

---

#### **4. Testing Infrastructure**

- **Changes**:
    - Introduced `FakeCatalog` implementing `SupermarketCatalog` for in-memory testing.
    - Added input validation (e.g., `price <= Decimal(0)` raises errors).

- **Impact**:
    - **Testability**: Enables unit tests without database dependencies.
    - **Fault Isolation**: Validation ensures invalid data fails fast during testing.

---

#### **5. Code Structure & Readability**

- **Changes**:
    - Split monolithic classes into focused components (e.g., `ReceiptPrinter` for formatting).
    - Used Python 3.8+ features like the walrus operator (`if offer := offers.get(product)`).
    - Added **docstrings** explaining class/method purposes.

- **Impact**:
    - **Maintainability**: Smaller, focused classes are easier to debug and extend.
    - **Clarity**: Code intent is immediately obvious to new developers.

---

#### **6. Error Handling**

- **Changes**:
    - Replaced generic `Exception` with specific errors (e.g., `ValueError("Quantity must be positive")`).
    - Added validation at object creation (e.g., `Product.__post_init__`).

- **Impact**:
    - **Fail-Fast Design**: Invalid usage is caught at the earliest possible stage.
    - **Debugging**: Specific exceptions pinpoint root causes.

---
