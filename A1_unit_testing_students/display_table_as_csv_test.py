import unittest
from unittest.mock import patch, mock_open

import pytest

from products import display_csv_as_table  # Replace 'your_module' with the actual module name
import io
import csv
import shutil
import os
class TestDisplayCSVAsTable(unittest.TestCase):

    @pytest.fixture
    def copy_csv_file(self):
        with open('copyproducts.csv', 'w', newline='') as csvfile:
            pass
        shutil.copy('products.csv', 'copyproducts.csv')

    '''def test_display_csv_valid_file(self):
        # Test with a valid CSV file
        csv_filename = 'valid_test_file.csv'
        with patch('builtins.open', side_effect=mock_open(read_data="header1,header2,header3\nvalue1,value2,value3")):
            # Here, 'mock_open' is a mock object to simulate opening the file
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                display_csv_as_table(csv_filename)
                # Assert that the correct output was printed to stdout
                self.assertEqual(mock_stdout.getvalue(), "header1,header2,header3\nvalue1,value2,value3\n")

    def test_display_csv_invalid_file(self):
        # Test with a non-existent file
        csv_filename = 'nonexistent_file.csv'
        with self.assertRaises(FileNotFoundError):
            display_csv_as_table(csv_filename)

    def test_display_csv_invalid_content(self):
        # Test with a CSV file containing invalid content
        csv_filename = 'invalid_content.csv'
        with patch('builtins.open', side_effect=mock_open(read_data="invalid content")):
            with self.assertRaises(csv.Error):
                display_csv_as_table(csv_filename)'''

    def test_display_csv_valid_file(self):
        # Test with a valid CSV file
        csv_filename = 'products.csv'
        with patch('builtins.open', side_effect=mock_open(read_data="header1,header2, header3\nvalue1,value2, value3")):
            # Here, 'mock_open' is a mock object to simulate opening the file
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                display_csv_as_table(csv_filename)
    def test_display_csv_valid_print(self):
        # Test with a valid CSV file
        csv_filename = 'products.csv'
        with patch('builtins.open', side_effect=mock_open(read_data="header1,header2, header3\nvalue1,value2, value3")):
            # Here, 'mock_open' is a mock object to simulate opening the file
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                display_csv_as_table(csv_filename)
                # Assert that the correct output was printed to stdout
                self.assertEqual(mock_stdout.getvalue(), "['header1', 'header2', ' header3']\n['value1', 'value2', ' value3']\n")
    def test_not_exists(self):
        csv_filename = './invalidfile.csv'
        self.assertEqual(False, os.path.isfile(csv_filename))

    def test_exists(self):
        csv_filename = './products.csv'
        self.assertEqual(True, os.path.isfile(csv_filename))


    # Add more test cases to cover other scenarios, such as empty file, malformed CSV, etc.

    #os.remove('copyproducts.csv')

if __name__ == '__main__':
    unittest.main()

