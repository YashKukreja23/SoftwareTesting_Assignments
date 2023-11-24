import json
import pytest
from unittest.mock import patch, mock_open
from login import is_valid_password, login_or_register

# Fixture for file operations stub
@pytest.fixture
def open_file_stub():
    data = [{"username": "testuser", "password": "Test@123", "wallet": 100}]
    with patch('builtins.open', mock_open(read_data=json.dumps(data))) as mock_open_file:
        yield mock_open_file

# Fixture for password validation stub (correct password)
@pytest.fixture
def check_password_stub_correct(mocker):
    return mocker.patch('login.is_valid_password', return_value=True)

# Fixture for password validation stub (incorrect password)
@pytest.fixture
def check_password_stub_incorrect(mocker):
    return mocker.patch('login.is_valid_password', return_value=False)

# Fixture for user input stub
@pytest.fixture
def user_input_stub(mocker):
    inputs = iter(["YashKukrejaST", "Testcase@12"])
    mocker.patch('login.get_user_input', side_effect=lambda _: next(inputs))

# Fixture for new user valid password stub
@pytest.fixture
def new_user_valid_password_stub(mocker):
    inputs = iter(["NewUser", "", "Y", "CorrectPass2!"])
    mocker.patch('login.get_user_input', side_effect=lambda _: next(inputs))
    mocker.patch('login.is_valid_password', return_value=True)

# Fixture for new user invalid password stub
@pytest.fixture
def new_user_invalid_password_stub(mocker):
    inputs = iter(["NewUser", "", "Y", "IncorrectPass"])
    mocker.patch('login.get_user_input', side_effect=lambda _: next(inputs))
    mocker.patch('login.is_valid_password', return_value=False)

def test_valid_login(user_input_stub, open_file_stub, check_password_stub_correct):
    with patch('builtins.print') as mock_print:
        user_info = login_or_register()

    assert user_info == {"username": "YashKukrejaST", "wallet": 100}
    assert "Successfully logged in" in mock_print.mock_calls[0].args[0]
    check_password_stub_correct.assert_called_with("Testcase@12")

def test_valid_registration(user_input_stub, open_file_stub, new_user_valid_password_stub):
    with patch('builtins.print') as mock_print:
        user_info = login_or_register()

    assert user_info == {"username": "NewUser", "wallet": 0}
    assert "Registration successful" in mock_print.mock_calls[0].args[0]

def test_invalid_password_registration(user_input_stub, open_file_stub, new_user_invalid_password_stub):
    with patch('builtins.print') as mock_print:
        user_info = login_or_register()

    assert user_info is None
    assert "Invalid password" in mock_print.mock_calls[0].args[0]
