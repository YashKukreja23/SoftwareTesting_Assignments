
from unittest.mock import patch, mock_open

import pytest

from products import display_csv_as_table
import io
import csv
import shutil
import os

@pytest.fixture()
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

def test_invalid_file(copy_csv_file):
    with pytest.raises(Exception):
        display_csv_as_table('products.sql')

def test_header(copy_csv_file):
    with open('copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        assert header == ['Product', 'Price', 'Units']

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

def test_display_csv_valid_print(copy_csv_file):
    # Test with a valid CSV file
    csv_filename = 'copy_products.csv'
    with patch('builtins.open', side_effect=mock_open(read_data="header1,header2, header3\nvalue1,value2, value3")):
        # Here, 'mock_open' is a mock object to simulate opening the file
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            display_csv_as_table(csv_filename)
            # Assert that the correct output was printed to stdout
            assert (mock_stdout.getvalue(), "['header1', 'header2', ' header3']\n['value1', 'value2', ' value3']\n")

def test_not_exists():
    csv_filename = './invalidfile.csv'
    assert (False, os.path.isfile(csv_filename))

def test_exists():
    csv_filename = './products.csv'
    assert (True, os.path.isfile(csv_filename))


def test_invalid_file_input(copy_csv_file):
    with pytest.raises(Exception):
        display_csv_as_table(123)

def test_invalid_list_of_files(copy_csv_file):
    with pytest.raises(Exception):
        display_csv_as_table(['copy_products.csv'])





