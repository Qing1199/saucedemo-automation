# tests/test_data/checkout_data.py

# Valid customer info
VALID_CUSTOMER = {
    "first_name": "John",
    "last_name":  "Doe",
    "postal_code": "12345"
}

# Invalid scenarios for checkout form
INVALID_CHECKOUT_DATA = [
    (
        "",
        "Doe",
        "12345",
        "First Name is required",
        "missing_first_name"
    ),
    (
        "John",
        "",
        "12345",
        "Last Name is required",
        "missing_last_name"
    ),
    (
        "John",
        "Doe",
        "",
        "Postal Code is required",
        "missing_postal_code"
    ),
]