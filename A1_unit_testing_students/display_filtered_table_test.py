
import pytest
from products import display_filtered_table
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
        display_filtered_table('products.sql', '')

def test_invalid_file_input(copy_csv_file):
    with pytest.raises(Exception):
        display_filtered_table(123, '')

def test_invalid_list_of_files(copy_csv_file):
    with pytest.raises(Exception):
        display_filtered_table(['copy_products.csv'], '')

def test_header(copy_csv_file):
    with open('copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        assert header == ['Product', 'Price', 'Units']

def test_search(copy_csv_file):
    assert ('Apple', display_filtered_table('copy_products.csv', 'Apple'))
    assert ('Backpack', display_filtered_table('copy_products.csv', 'Backpack'))
    assert ('Dumbbells', display_filtered_table('copy_products.csv', 'Dumbbells'))
    assert ('Hat', display_filtered_table('copy_products.csv', 'Hat'))
    assert ('Cereal', display_filtered_table('copy_products.csv', 'Cereal'))

def test_invalid_input(copy_csv_file):
    assert '2' != display_filtered_table('copy_products.csv', 'Apple')
    assert '1' != display_filtered_table('copy_products.csv', 'Banana')
    assert '0.8' != display_filtered_table('copy_products.csv', 'Onion')
    assert '0.75' != display_filtered_table('copy_products.csv', 'Potato')
    assert '3' != display_filtered_table('copy_products.csv', 'Juice')

def test_missing_input(copy_csv_file):
    assert ('', display_filtered_table('copy_products.csv', 'Saxophone'))
    assert ('', display_filtered_table('copy_products.csv', 'Stairs'))
    assert ('', display_filtered_table('copy_products.csv', 'Sprite'))
    assert ('', display_filtered_table('copy_products.csv', 'Steak'))
    assert ('', display_filtered_table('copy_products.csv', 'BeerPong'))

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

def test_not_exists():
    csv_filename = './invalidfile.csv'
    assert (False, os.path.isfile(csv_filename))

def test_exists():
    csv_filename = './products.csv'
    assert (True, os.path.isfile(csv_filename))