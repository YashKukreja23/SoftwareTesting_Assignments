from checkout_and_payment import *
import pytest
import os
import csv
import shutil
from unittest.mock import *
from products import *


from unittest.mock import patch
from checkout_and_payment import check_cart, User, ShoppingCart, Product

##LOAD PRODUCTS FROM CSV
@pytest.fixture
def load_csv():
    shutil.copy('products.csv', 'products_remove.csv')
    yield 
    #remove the copied CSV file
    os.remove('products_remove.csv')

#other method found online    
# @pytest.fixture
# def load_product_stub(mocker):
#     return mocker.patch('checkout_and_payment.load_products_from_csv', return_value=products)


#For header
def correct_header(load_csv):
    with open('products_remove.csv', 'r', newline='') as csvfile:
        read_csv = csv.reader(csvfile)
        header = next(read_csv)
        assert header == ['Product', 'Price', 'Units']

#testing if correct product is fetched
def valid_product(load_csv):
    productsTest = load_products_from_csv('products_remove.csv')

    assert len(products) == 63


#For wrong header
def test_load_products_from_csv_wrong_headers(load_products_from_csv, capsys):
    #need to change the name of the headers first in the csv file
    with pytest.raises(SystemExit):
        load_products_from_csv("products.csv")

    # Check that the correct error message is printed
    captured = capsys.readouterr()
    assert "Error: Incorrect CSV headers. Expected ['Name', 'Price', 'Units']" in captured.err

#check if no file exists:

def test_empty_file():
    assert load_products_from_csv("") == "Cannot find file"

#check of file is wrong
def test_wrong_file():
    assert load_products_from_csv("wrong.csv") == "Cannot find file"

#test if it breaks on float value
def float_type_test():
    with pytest.raises(Exception):
        load_products_from_csv(0.5)


# Check if the products are loaded with correct name, quantity and price
def test_load_products():
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
    assert checkout(mock_users("Prachi", 50), empty_cart, cart_shopping(None)) == "Cart is empty. Please add items before chekout."


def negative_wallet():
    assert checkout(mock_users("Prachi", -7), cart_shopping(mock_product("Apple", 30, 4))) == ("Negative wallet amount.")

def no_money_wallet():
    assert checkout(mock_users("Prachi", -7), cart_shopping(mock_product("Apple", 30, 4))) == ("No money in wallet.")

# Product should be removed if units = 0
def checkout_product_last_item():
    products_in_list = products.copy()
    adding_product = mock_product("MockProduct", 55, 6)
    products.append(adding_product)
    assert len(products_in_list) == len(products) - 6



##CART

#trying another method
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


#check if the cart is empty
def cart_empty(mock_user, mock_product, mock_input):
    mock_product.clear_items()
    check_cart(mock_user, mock_product)
    mock_input.side_effect = ["y"]


#Check the cart if said yes to checkout
def checkout_from_cart(mock_user, mock_product, mock_input):
    assert_thing = check_cart(mock_user, mock_product)
    mock_input.side_effect = ["y"]
    assert assert_thing is None


#check if any input is invalid
def invalid_input_while_checkout(mock_user, mock_product, mock_input):
    assert_thing = check_cart(mock_user, mock_product)
    mock_input.side_effect = ["Invalid"]
    assert assert_thing is False


