import pytest
from unittest.mock import Mock, patch
from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from checkout_and_payment import *
from logout import logout
from products import *
import shutil
import os
import io
import json
from _pytest import monkeypatch
from unittest.mock import patch
from unittest.mock import patch, mock_open
from login import login_or_register
from itertools import cycle
from unittest import mock
import checkout_and_payment
import products

#Checkout and payment
@pytest.fixture(scope='module')
def user_dummmy_file():
    shutil.copy('users.json', 'dummy_users.json')
    print("Dummy file created")
    yield

    os.remove('dummy_users.json')
    print("Dummy file removed")


# Check user registration
@pytest.fixture
def check_user_registered():
    return {"username": "Simba", "password": "LionKing@^456", "wallet": 100}


# Open file stub
@pytest.fixture
def open_file_stub(monkeypatch, user_registered):
    read_data = json.dumps([user_registered])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))


# Magic mock JSON
@pytest.fixture
def json_dump_mocked(monkeypatch):
    mock_test = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_test)
    return mock_test


# Logout stub
@pytest.fixture
def stub_logout(mocker):
    return mocker.patch('logout.logout', return_value=True)


# Fake input
def fake_input(input_list):
    i = 0

    def _fake_input(foo_bar):
        nonlocal i
        mimicked_input = input_list[i]
        i += 1
        return mimicked_input

    return _fake_input

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

#Test several products
def test_several_products(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Banana - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]

def test_other_letter(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["a", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "\nInvalid input. Please try again.\nYou have been logged out\n"
    assert output in out

#Test other number
def test_other_number(capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["5", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "\nInvalid input. Please try again.\nYou have been logged out\n"
    assert output in out

def logout_confirmed(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "You have been logged out for the system."
    assert output in out[:28]

#Test add item to cart
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

#Display filtered table
@pytest.fixture()
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

def test_invalid_file(copy_csv_file):
    with pytest.raises(Exception):
        display_filtered_table('products.sql', '')

def test_invalid_file_input(copy_csv_file):
    with pytest.raises(Exception):
        display_filtered_table(123, '')

def test_invalid_list_of_files(copy_csv_file):
    with pytest.raises(Exception):
        display_filtered_table(['copy_products.csv'], '')

def test_rows(copy_csv_file):
    with open('copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        count = 5
        while count < 0:
            if count == 5:
                assert (csv_reader[count],['Strawberry', '4', '12'])
            if count == 4:
                assert (csv_reader[count],['Grapes', '3', '5'])
            if count == 3:
                assert (csv_reader[count],['Orange', '1.5', '8'])
            if count == 2:
                assert (csv_reader[count],['Banana', '1', '15'])
            if count == 1:
                assert (csv_reader[count],['Apple', '2', '10'])

def test_header(copy_csv_file):
    with open('copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        assert header == ['Product', 'Price', 'Units']

#Display table as CSV
def test_not_exists():
    csv_filename = './invalidfile.csv'
    assert (False, os.path.isfile(csv_filename))

def test_exists():
    csv_filename = './products.csv'
    assert (True, os.path.isfile(csv_filename))

def test_invalid_float(copy_csv_file):
    with pytest.raises(Exception):
        display_csv_as_table(0.5)

def test_invalid_bool(copy_csv_file):
    with pytest.raises(Exception):
        display_csv_as_table(True)

def test_display_csv_valid_print(copy_csv_file):
    # Test with a valid CSV file
    csv_filename = 'copy_products.csv'
    with patch('builtins.open', side_effect=mock_open(read_data="header1,header2, header3\nvalue1,value2, value3")):
        # Here, 'mock_open' is a mock object to simulate opening the file
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            display_csv_as_table(csv_filename)
            # Assert that the correct output was printed to stdout
            assert (mock_stdout.getvalue(), "['header1', 'header2', ' header3']\n['value1', 'value2', ' value3']\n")

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

#Search and buy product
@pytest.fixture
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

@pytest.fixture
def display_csv_as_table_mock(mocker):
    return mocker.patch('products.display_csv_as_table', return_value = None)

@pytest.fixture
def display_filtered_table_mock(mocker):
    return mocker.patch('products.display_filtered_table', return_value = None)

@pytest.fixture
def input_stub1(mocker):
    values = ['all', 'y']
    return mocker.patch("builtins.input", side_effects = values)

@pytest.fixture
def checkout_and_payment_mock(mocker):
    return mocker.patch('checkout_and_payment.checkoutAndPayment', return_value = None)

def test_display_csv_as_table(mocker, copy_csv_file):
    m = mocker.MagicMock(return_value = None)
    mocker.patch('products.display_csv_as_table', m)
    products.display_csv_as_table(copy_csv_file)
    m.assert_called_once()

def test_display_filtered_table(mocker, copy_csv_file):
    m = mocker.MagicMock(return_value = None)
    mocker.patch('products.display_filtered_table', m)
    products.display_filtered_table(copy_csv_file, 'Apple')
    m.assert_called_once()


def test_checkout_and_payment(mocker):
    m = mocker.MagicMock(return_value = None)
    mocker.patch('checkout_and_payment.checkoutAndPayment', m)
    checkout_and_payment.checkoutAndPayment()
    m.assert_called_once()

#Load products from CSV
@pytest.fixture
def load_csv():
    shutil.copy('products.csv', 'products_remove.csv')
    yield
    #remove the copied CSV file
    os.remove('products_remove.csv')

def test_empty_file():
    with pytest.raises(Exception):
        load_products_from_csv("")

def test_wrong_file():
    with pytest.raises(Exception):
        load_products_from_csv("wrong.csv")


def test_load_products_with_values():
    productsTest_values = load_products_from_csv("products.csv")

    assert productsTest_values[0].name == "Apple"
    assert productsTest_values[0].price == 2
    assert productsTest_values[0].units == 10

