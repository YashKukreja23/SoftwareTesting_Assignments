import pytest
from unittest.mock import Mock, patch
from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from checkout_and_payment import *
from logout import logout
from products import *
import shutil
import os
import json
from _pytest import monkeypatch
from unittest.mock import patch
from login import login_or_register
from itertools import cycle

#CHECKOUT AND PAYMENT
# Dummy user file
@pytest.fixture(scope='module')
def user_dummmy_file():
    """
    Fixture providing a dummy user file for testing purposes.

    This fixture sets up a dummy user file that can be used in test cases
    to simulate scenarios related to user data.

    Returns:
        str: The path to the dummy user file.
    """
    shutil.copy('users.json', 'dummy_users.json')
    print("Dummy file created")
    yield
    os.remove('dummy_users.json')
    print("Dummy file removed")


# Check user registration
@pytest.fixture
def check_user_registered():
    """
    Fixture to check user registration status.

    This fixture can be used to check if a user is registered by interacting
    with the system or database.

    Returns:
        bool: True if the user is registered, False otherwise.
    """
    return {"username": "Simba", "password": "LionKing@^456", "wallet": 100}


# Open file stub
@pytest.fixture
def open_file_stub(monkeypatch, user_registered):
    """
    Fixture providing a stub for file opening.

    This fixture can be used to replace actual file opening operations
    with a stub for testing purposes.

    Returns:
        object: A file-like object or stub for file opening.
    """
    read_data = json.dumps([user_registered])
    monkeypatch.setattr('builtins.open', Mock(mock_open=mock.mock_open(read_data=read_data)))


# Magic mock JSON
@pytest.fixture
def json_dump_mocked(monkeypatch):
    """
    Fixture providing a mocked JSON dump.

    This fixture can be used to replace the actual JSON dump operation
    with a mocked version for testing purposes.

    Returns:
        str: Mocked JSON data.
    """
    mock_test = Mock()
    monkeypatch.setattr('json.dump', mock_test)
    return mock_test


# Logout stub
@pytest.fixture
def stub_logout(mocker):
    """
    Fixture providing a stub for user logout.

    This fixture can be used to replace actual user logout operations
    with a stub for testing purposes.

    Returns:
        bool: True if the logout is successful, False otherwise.
    """
    return mocker.patch('logout.logout', return_value=True)


# Define the mocker fixture
@pytest.fixture
def mocker():
    return Mock()


# Fake input
def fake_input(input_list):
    i = 0

    def _fake_input(foo_bar):
        nonlocal i
        mimicked_input = input_list[i]
        i += 1
        return mimicked_input

    return _fake_input


# Login confirmed
def logout_confirmed(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "You have been logged out for the system."
    assert output in out[:28]


# Test add item to cart
def test_add_item(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack added to your cart."
    assert output in out[30:]


# Test out of stock
def test_out_of_stock(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack is out of stock."
    assert output in out[30:]

# Test several products
def test_several_products(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Banana - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]

# Test other letter
def test_other_letter(stub_logout, capsys, monkeypatch, mocker):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["a", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again.\nYou have been logged out"
    actual_output = out.strip()  # Strip leading and trailing whitespaces
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    assert expected_output in actual_output

# Test other number
def test_other_number(capsys, monkeypatch, mocker):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["5", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again.\nYou have been logged out"
    actual_output = out.strip()  # Strip leading and trailing whitespaces
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    assert expected_output in actual_output

@pytest.fixture
def mock_search_and_buy(mocker):
    return mocker.patch('products.searchAndBuyProduct')

@pytest.fixture
def mocker_display_csv(mocker):
    return mocker.patch('products.display_csv_as_table')

@pytest.fixture
def mocker_display_filtered(mocker):
    return mocker.patch('products.display_filtered_table')



def test_open_file():
    try:
        with open("products.csv", 'r') as file:
            content = file.read()
        assert True is True
    except Exception as e:
        assert True is False

def test_csv_table_header_display(capsys):
    display_csv_as_table("products.csv")
    captured = capsys.readouterr()
    assert captured.out[0:29] == "['Product', 'Price', 'Units']"

def test_csv_table_header_filter(capsys):
    display_filtered_table("products.csv", 'Potato')
    captured = capsys.readouterr()
    assert captured.out[0:29] == "['Product', 'Price', 'Units']"

def test_fake_file():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("this_file_is_not_real.csv")
        display_filtered_table("this_file_is_also_not_real.csv","Potato")

def test_logout(capsys):
    with patch('builtins.input', side_effect=["Ramanathan", "Notaproblem23*", 'all', 'y', 'l']):
        with pytest.raises(StopIteration):
            searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Login or registration canceled.\n" in captured.out
from checkout_and_payment import check_cart, User, ShoppingCart, Product

# test if it breaks on float value
def float_type_test():
    with pytest.raises(Exception):
        load_products_from_csv(0.5)


# Check if the products are loaded with correct name, quantity and price
def test_load_products():
    number_of_products=10
    productsTest = load_products_from_csv("products.csv")
    for i in range(number_of_products):
        assert productsTest[i].name == productsTest[i].name
        assert productsTest[i].units == productsTest[i].units
        assert productsTest[i].price == productsTest[i].price


# Check if the products are loaded with correct name, quantity and price
def test_load_products_with_values():
    productsTest_values = load_products_from_csv("products.csv")

    assert productsTest_values[0].name == "Apple"
    assert productsTest_values[0].price == 2
    assert productsTest_values[0].units == 10


##CHECKOUT

@pytest.fixture
def mock_print(mocker):
    return mocker.patch('checkout_and_payment.checkout', return_value="")


def mock_users(username, userwallet):
    return user(username, userwallet)


def mock_product(name, price, units):
    return product(name, price, units)


def cart_shopping(product):
    cart_test = ShoppingCart()
    if product is not None:
        cart_test.add_item(product)
    return cart_test


def empty_cart():
    assert checkout(mock_users("Prachi", 50), cart_shopping(None)) == "Empty Cart Test"


def empty_cart_checkout():
    assert checkout(mock_users("Prachi", 50), empty_cart,
                    cart_shopping(None)) == "Cart is empty. Please add items before chekout."


def negative_wallet():
    assert checkout(mock_users("Prachi", -7), cart_shopping(mock_product("Apple", 30, 4))) == (
        "Negative wallet amount.")


def no_money_wallet():
    assert checkout(mock_users("Prachi", -7), cart_shopping(mock_product("Apple", 30, 4))) == ("No money in wallet.")


# Product should be removed if units = 0
def checkout_product_last_item():
    products_in_list = products.copy()
    adding_product = mock_product("MockProduct", 55, 6)
    products.append(adding_product)
    assert len(products_in_list) == len(products) - 6


##CART

# trying another method
@pytest.fixture
def mock_print(mocker):
    return mocker.patch('checkout_and_payment.cart', return_value="")


@pytest.fixture
def mock_input(mocker):
    return mocker.patch("builtins.input")


@pytest.fixture
def mock_users(username, userwallet):
    return User("Prachi", 40.0)


@pytest.fixture
def mock_product():
    mock_cart = ShoppingCart()
    mock_cart.add_item(Product("Apple", 20, 20))
    mock_cart.add_item(Product("Banana", 10, 20))
    return mock_cart


# check if the cart is empty
def cart_empty(mock_user, mock_product, mock_input):
    mock_product.clear_items()
    check_cart(mock_user, mock_product)
    mock_input.side_effect = ["y"]


# Check the cart if said yes to checkout
def checkout_from_cart(mock_user, mock_product, mock_input):
    assert_thing = check_cart(mock_user, mock_product)
    mock_input.side_effect = ["y"]
    assert assert_thing is None


# check if any input is invalid
def invalid_input_while_checkout(mock_user, mock_product, mock_input):
    assert_thing = check_cart(mock_user, mock_product)
    mock_input.side_effect = ["Invalid"]
    assert assert_thing is False


#Login

@pytest.fixture
def open_file_stub():
    data = [{"username": "testuser", "password": "Test@123", "wallet": 100}]
    with patch('builtins.open', create=True) as mock_open_file:
        mock_open_file.return_value.__enter__.return_value.read.return_value = json.dumps(data)
        yield mock_open_file

# Fixture for user input stub
@pytest.fixture
def user_input_stub():
    inputs = cycle(["TestUser", "Test@123"])
    with patch('builtins.input', side_effect=lambda _: next(inputs)):
        yield

# Fixture for new user valid password stub
@pytest.fixture
def new_user_valid_password_stub():
    inputs = cycle(["NewUser", "", "yes", "CorrectPass2!"])
    with patch('builtins.input', side_effect=lambda _: next(inputs)):
        with patch('login.is_valid_password', return_value=True):  # Adjust the module reference here
            yield

# Fixture for new user invalid password stub
@pytest.fixture
def new_user_invalid_password_stub():
    inputs = cycle(["NewUser", "", "yes", "invalid"])
    with patch('builtins.input', side_effect=lambda _: next(inputs)):
        with patch('login.is_valid_password', return_value=False):  # Adjust the module reference here
            yield

def test_valid_registration(open_file_stub, new_user_valid_password_stub):
    with patch('builtins.print') as mock_print:
        user_info = login_or_register()

    assert user_info == {"username": "NewUser", "wallet": 0}
    assert "Registration successful" in mock_print.mock_calls[0].args[0]

def test_invalid_password_registration(open_file_stub, new_user_invalid_password_stub):
    with patch('builtins.print') as mock_print:
        user_info = login_or_register()

    assert user_info is None
    assert "Invalid password" in mock_print.mock_calls[0].args[0]


