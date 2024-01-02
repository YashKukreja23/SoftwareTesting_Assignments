from unittest.mock import patch
import pytest
from login import *
from products import *
from checkout_and_payment import *

@pytest.fixture
def end_to_end_shopping(monkeypatch):
    #user has a card
    user_inputs = iter(["Yashkuks", "YashKukreja2!","2","all","y","5","c","y","l"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs


@pytest.fixture
def end_to_end_shopping_not_buying(monkeypatch):
    user_inputs = iter(["Jorge", "passwrd1!","all","n","all","y","l"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs

@pytest.fixture
def end_to_end_logging_out_with_cart(monkeypatch):
    #User after adding product to cart  logging out without shoping
    user_inputs = iter(["Jorge", "passwrd1!", "all", "1","l","y"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs


@pytest.fixture
def end_to_end_check_empty_cart(monkeypatch):
    #User with empty cart logging out without shoping but checked
    user_inputs = iter(["Jorge", "passwrd1!","all","y","c","b","l"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs

@pytest.fixture
def end_to_end_shopping_by_inputting_invalid_password(monkeypatch):
    user_inputs = iter(["Jorge", "aaaaa", "no"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs

@pytest.fixture
def end_to_end_bad_registration(monkeypatch):
    user_inputs = iter(["dad", "a", "y"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs

@pytest.fixture
def end_to_end_shopping_checking_out_empty_cart(monkeypatch):
    #user has a card
    user_inputs = iter(["Yashkuks", "YashKukreja2!", "all", "y", "c", "c", "l"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs

@pytest.fixture
def end_to_end_shopping_insufficient_funds(monkeypatch):
    #user has a card
    user_inputs = iter(["Yashkuks", "YashKukreja2!","all","TV","55","c","c","wallet","l","y"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(user_inputs))
    return user_inputs


def test_end_to_end_check_empty_cart(end_to_end_check_empty_cart):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()

    # Assert that the function display the expected result
    mock_print.assert_called_with("You have been logged out")

def test_end_to_end_shopping_not_buying(end_to_end_shopping_not_buying):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    # Assert that the function display the expected result
    mock_print.assert_called_with("You have been logged out")

def test_end_to_end_shopping_by_inputting_invalid_password(end_to_end_shopping_by_inputting_invalid_password):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    mock_print.assert_any_call("Login or registration canceled.")


def test_end_to_end_shopping_insufficient_funds(end_to_end_shopping_insufficient_funds):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    mock_print.assert_any_call("You don't have enough money to complete the purchase.\nPlease try again!")
    # Assert that the function display the expected result
    mock_print.assert_called_with("You have been logged out")

def test_end_to_end_shopping_checking_out_empty_cart(end_to_end_shopping_checking_out_empty_cart):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    mock_print.assert_any_call("\nYour basket is empty. Please add items before checking out.")
    # Assert that the function display the expected result
    mock_print.assert_called_with("You have been logged out")


def test_end_to_end_bad_registration(end_to_end_bad_registration):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    mock_print.assert_any_call("Login or registration canceled.")


def test_end_to_end_logging_out_with_cart(end_to_end_logging_out_with_cart):
    # Use monkeypatch to replace the input function during the test
    with patch('builtins.print'):
        with patch('builtins.print') as mock_print:
            # Call the login function
            searchAndBuyProduct()
    mock_print.assert_any_call("Your cart is not empty.You have following items")
    # Assert that the function display the expected result
    mock_print.assert_called_with("You have been logged out")