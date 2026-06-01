# tests/test_data/login_data.py

# Each tuple = (username, password, expected_error_fragment, test_id)
INVALID_LOGIN_DATA = [
    (
        "",
        "secret_sauce",
        "Username is required",
        "empty_username"
    ),
    (
        "standard_user",
        "",
        "Password is required",
        "empty_password"
    ),
    (
        "standard_user",
        "wrong_password",
        "Epic sadface",
        "wrong_password"
    ),
    (
        "locked_out_user",
        "secret_sauce",
        "locked out",
        "locked_user"
    ),
    (
        "fake_name",
        "fake_password",
        "Username and password do not match",
        "fake_name_fake_password"
    ),
]