from unittest import mock

import pytest
from products import searchAndBuyProduct
import csv
import shutil
import os
import unittest.mock
from unittest.mock import patch
@pytest.fixture()
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

@patch('builtins.input', side_effect=['valid_username', 'valid_password', 'all', 'Y'])
@patch('products.display_csv_as_table')
@patch('products.checkoutAndPayment')
def test_search_and_buy_product_valid_inputs(mock_checkout, mock_display):
    searchAndBuyProduct()
    # Add assertions to check the expected behavior based on valid inputs

@patch('builtins.input', side_effect=['invalid_username', 'invalid_password', 'all', 'Y'])
def test_search_and_buy_product_invalid_login():
    # Test for invalid login input
    with pytest.raises(Exception):  # Adjust this to the actual exception type raised in your code
        searchAndBuyProduct()

def test_function():
    with mock.patch.object(__builtins__, 'input', lambda: 'some_input'):
        assert searchAndBuyProduct() == 'expected_output'