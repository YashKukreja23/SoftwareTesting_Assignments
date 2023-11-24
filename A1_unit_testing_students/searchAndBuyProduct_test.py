from unittest import mock

import pytest
from products import searchAndBuyProduct
import csv
import shutil
import os
import products
import checkout_and_payment
import unittest.mock
from unittest.mock import patch
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
