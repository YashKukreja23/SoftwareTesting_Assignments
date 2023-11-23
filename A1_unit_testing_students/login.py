import json
import re  # Import the regular expression module for password validation


# Function to validate password
def is_valid_password(password):
    # Check for at least 1 capital letter, at least one special symbol, and length at least 8
    return any(c.isupper() for c in password) and any(c in '!@#$%^&*()_-+=[]{}|;:,.<>?/' for c in password) and len(
        password) >= 8


# Function to perform login or registration
def login_or_register():
    username = input("Enter your username:")
    password = input("Enter your password:")

    with open('users.json', "r") as file:
        data = json.load(file)

        for entry in data:
            if entry["username"] == username and entry["password"] == password:
                print("Successfully logged in")
                return {"username": entry["username"], "wallet": entry["wallet"]}

        # If username is not found, ask if the user wants to register
        register = input("Username not found. Do you want to register? (yes/no): ")

        if register.lower() == 'yes':
            new_password = input("Enter your new password:")

            # Validate the new password
            if is_valid_password(new_password):
                new_user = {"username": username, "password": new_password, "wallet": 0}
                data.append(new_user)

                with open('users.json', 'w') as file:
                    json.dump(data, file, indent=2)

                print("Registration successful. You can now log in with your new credentials.")
                return {"username": new_user["username"], "wallet": new_user["wallet"]}
            else:
                print(
                    "Invalid password. Password must have at least 1 capital letter, at least one special symbol, and be at least 8 characters long.")
                return None
        else:
            print("Login or registration canceled.")
            return None


# Test the login_or_register function
'''user_info = login_or_register()
if user_info:
    print("User info:", user_info)'''
