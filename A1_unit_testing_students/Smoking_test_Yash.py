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


def test_end_to_end_scenario_1(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda x: "TestUser" if "Enter your username" in x else "Test@123")
    mocker_display_csv = mocker.patch('products.display_csv_as_table')
    mocker_login_or_register = mocker.patch('login.login_or_register')
    mocker_login_or_register.return_value = {"username": "TestUser", "wallet": 100}
    mocker_checkout_and_payment = mocker.patch('checkout_and_payment.checkoutAndPayment')

    searchAndBuyProduct()

    mocker_login_or_register.assert_called_once()
    mocker_display_csv.assert_called_once_with("products.csv")
    mocker_checkout_and_payment.assert_called_once_with({"username": "TestUser", "wallet": 100})


def test_end_to_end_scenario_2(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda x: "TestUser" if "Enter your username" in x else "Test@123")
    mocker_display_csv = mocker.patch('products.display_csv_as_table')
    mocker_display_filtered = mocker.patch('products.display_filtered_table')
    mocker_login_or_register = mocker.patch('login.login_or_register')
    mocker_login_or_register.return_value = {"username": "TestUser", "wallet": 100}
    mocker_checkout_and_payment = mocker.patch('checkout_and_payment.checkoutAndPayment')

    searchAndBuyProduct()

    mocker_login_or_register.assert_called_once()
    mocker_display_filtered.assert_called_once_with("products.csv", "SpecificProduct")
    mocker_checkout_and_payment.assert_called_once_with({"username": "TestUser", "wallet": 100})



def test_end_to_end_scenario_3(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', cycle(["InvalidUser", "InvalidPassword", "RetryUser", "Retry@123"]))
    mocker_display_csv = mocker.patch('products.display_csv_as_table')
    mocker_login_or_register = mocker.patch('login.login_or_register',
                                            side_effect=[None, None, {"username": "CorrectPass!", "wallet": 150}])
    mocker_checkout_and_payment = mocker.patch('checkout_and_payment.checkoutAndPayment')

    searchAndBuyProduct()

    assert mocker_login_or_register.call_count == 3
    mocker_display_csv.assert_called_once_with("products.csv")
    mocker_checkout_and_payment.assert_called_once_with({"username": "RetryUser", "wallet": 150})



def test_end_to_end_scenario_4(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda x: "TestUser" if "Enter your username" in x else "Test@123")
    mocker_display_csv = mocker.patch('products.display_csv_as_table')
    mocker_login_or_register = mocker.patch('login.login_or_register')
    mocker_login_or_register.return_value = {"username": "TestUser", "wallet": 100}
    mocker_logout = mocker.patch('logout.logout', return_value=True)

    searchAndBuyProduct()

    mocker_login_or_register.assert_called_once()
    mocker_display_csv.assert_called_once_with("products.csv")
    mocker_logout.assert_called_once()