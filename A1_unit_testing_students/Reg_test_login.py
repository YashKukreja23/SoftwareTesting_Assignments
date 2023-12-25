import pytest
from unittest.mock import patch
from login import is_valid_password, login_or_register

def input_side_effect(values):
    def side_effect(*args, **kwargs):
        if not values:
            return  # Indicate end of input values
        return values.pop(0)
    return side_effect

@pytest.mark.parametrize("input_values", [
    ['testuser', 'Test@123'],  # for test_valid_login
    ['nonexistent_user', 'IncorrectPass', 'no'],  # for test_invalid_login_and_cancel
    ['new_user', 'IncorrectPass', 'no'],  # for test_invalid_password_registration_and_cancel
    ['new_user', 'CorrectPass2!', 'yes'],  # for test_successful_registration
    ['new_user', 'IncorrectPass', 'yes'],  # for test_invalid_password_registration
])
def test_valid_login(input_values):
    with patch('builtins.input', side_effect=input_side_effect(input_values)):
        user_info = login_or_register()
        assert user_info is not None
        assert user_info['username'] == 'testuser'  # Update accordingly

@pytest.mark.parametrize("input_values", [
    ['testuser', 'IncorrectPass', 'no'],  # for test_invalid_login_and_cancel
])
def test_invalid_login_and_cancel(input_values):
    with patch('builtins.input', side_effect=input_side_effect(input_values)):
        result = login_or_register()
        assert result is None

@pytest.mark.parametrize("input_values", [
    ['new_user', 'IncorrectPass', 'no'],  # for test_invalid_password_registration_and_cancel
])
def test_invalid_password_registration_and_cancel(input_values):
    with patch('builtins.input', side_effect=input_side_effect(input_values)):
        result = login_or_register()
        assert result is None

@pytest.mark.parametrize("input_values", [
    ['new_user', 'CorrectPass2!', 'yes'],  # for test_successful_registration
])
def test_successful_registration(input_values):
    with patch('builtins.input', side_effect=input_side_effect(input_values)):
        result = login_or_register()
        assert result is not None
        assert result['username'] == 'NewUser'  # Update accordingly

@pytest.mark.parametrize("input_values", [
    ['new_user', 'IncorrectPass', 'yes'],  # for test_invalid_password_registration
])
def test_invalid_password_registration(input_values):
    with patch('builtins.input', side_effect=input_side_effect(input_values)):
        result = login_or_register()
        assert result is None

