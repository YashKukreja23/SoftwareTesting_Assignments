import json
import pytest
from itertools import cycle
from unittest.mock import patch
from login import login_or_register

# Fixture for file operations stub
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

