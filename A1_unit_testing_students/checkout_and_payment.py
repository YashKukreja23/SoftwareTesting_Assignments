import csv
from logout import logout

# User class to represent user information
class User:
    def __init__(self, name, wallet, cards=None):
        self.name = name
        self.wallet = float(wallet)
        self.cards = cards if cards is not None else []

# Product class to represent product information
class Product:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)

    # A method to get product details as a list
    def get_product(self):
        return [self.name, self.price, self.units]

    def increment_units(self):
        self.units += 1

    def __str__(self):
        return f'[{self.name}, {self.price}, {self.units}]'


# ShoppingCart class to represent the user's shopping cart
class ShoppingCart:
    def __init__(self):
        self.items = []

    # Method to add a product to the cart
    def add_item(self, product):
        self.items.append(product)

    # Method to remove a product from the cart
    def remove_item(self, product):
        self.items.remove(product)

    # Method to retrieve the items in the cart
    def retrieve_item(self):
        return self.items

    # Method to clear all items from the cart
    def clear_items(self):
        self.items = []

    # Method to calculate the total price of items in the cart
    def get_total_price(self):
        return sum(item.price for item in self.items)


# Function to load products from a CSV file
def load_products_from_csv(file_path):
    products = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(Product(row['Product'], row['Price'], row['Units']))
    return products


# Load products from the CSV file
products = load_products_from_csv("products.csv")
cart = ShoppingCart()


# Function to complete the checkout process
def checkout(user, cart, inputs=None):
    if inputs is None:
        inputs = input  # Use the default input function if not provided

    if not cart.items:
        print("\nYour basket is empty. Please add items before checking out.")
        return

    total_price = cart.get_total_price()
    question_payment = inputs("Do you want to pay with wallet or credit card?")
    if question_payment.lower() == "credit":
        print("\nYour Cards:")
        for i, card in enumerate(user.cards, start=1):
            print(f"{i}. {card}")

        while True:
            try:
                card_index = int(inputs("Select a card (enter the card number): ")) - 1
                if 0 <= card_index < len(user.cards):
                    print("Thank you for your payment.")
                    break
                else:
                    print("Invalid card selection. Please choose a valid card.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:
        if total_price > user.wallet:
            print("\nYou don't have enough money to complete the purchase.")
            print("Please try again!")
        else:
            # Deduct the total price from the user's wallet
            user.wallet -= total_price
            # Update product units and remove products with zero units
            for item in cart.items:
                item.units -= 1
                if item.units == 0:
                    products.remove(item)
            # Clear the cart
            cart.items = []

            # Print a thank you message with the remaining balance
            print("\nThank you for your purchase, {}! Your remaining balance is {}".format(user.name, user.wallet))


# Function to check the cart and proceed to checkout if requested
'''def check_cart(user, cart):
    # Print products in the cart
    for i in cart.retrieve_item():
        print(i.get_product())
    # Ask the user if they want to checkout
    question = input("Do you want to checkout (Y/N)?")
    if question.lower() == "y":
        return checkout(user, cart)
    else:
        return False'''


def get_item_cart(cart, product_name):
    for item in cart.items:
        if item.name.lower() == product_name.lower():
            return item
    return None

def remove_item_from_cart(self, product):
    if product in self.items:
        self.items.remove(product)
        product.increment_units()
        print(f"{product} removed from your cart.")
    else:
        print(f"{product} is not in your cart.")

    print("\nRemaining items in your cart:")
    for i in cart.retrieve_item():
        print(i.get_product())

    return True if product else False

def check_cart(user, cart):
    while True:
        # Print products in the cart
        for i, product in enumerate(cart.retrieve_item()):
            print(f"{i + 1}. {product.name} - ${product.price} - Units: {product.units}")

        # Ask the user if they want to query, remove, or checkout
        question = input("Enter the product number to query (Q), remove (R), checkout (C), or go back (B): ").lower()

        if question == 'q':
            # Query individual item details
            product_number = int(input("Enter the product number to query: "))
            if 1 <= product_number <= len(cart.items):
                queried_product = cart.items[product_number - 1]
                print(f"{queried_product.name} - ${queried_product.price} - Units: {queried_product.units}")
            else:
                print("Invalid product number.")
        elif question == 'r':
            # Remove individual item from the cart
            product_number = int(input("Enter the product number to remove: "))
            if 1 <= product_number <= len(cart.items):
                removed_product = cart.items[product_number - 1]
                remove_item_from_cart(cart, removed_product)
            else:
                print("Invalid product number.")
        elif question == 'c':
            # Proceed to checkout
            return checkout(user, cart)
        elif question == 'b':
            # Go back to product selection
            break
        else:
            print("Invalid input. Please try again.")


# Main function for the shopping and checkout process
def checkoutAndPayment(login_info):
    # Create/retrieve a user using login information
    username = login_info["username"]
    wallet = login_info["wallet"]
    cards = ["8123 1232 1273 1238", "1234 5678 9012 3456"]  # Hardcoded card details

    user = User(username, wallet, cards)

    # Display available products
    for i, product in enumerate(products):
        print(f"{i + 1}. {product.name} - ${product.price} - Units: {product.units}")

    while True:
        # Get user input for product selection in numbers
        choice = input("\nEnter the product number you want to add to your cart (c to check cart, l to logout): ")

        if choice == 'c':
            # Check the cart and proceed to checkout if requested
            check = check_cart(user, cart)
            if check is False:
                continue
        elif choice == 'l':
            # Logout the user
            ask_logout = logout(cart)
            if ask_logout is True:
                print("You have been logged out")
                break
            else:
                continue
        elif choice.isdigit() and 1 <= int(choice) <= len(products):
            # Add the selected product to the cart
            selected_product = products[int(choice) - 1]
            if selected_product.units > 0:
                cart.add_item(selected_product)
                print(f"{selected_product.name} added to your cart.")
            else:
                print(f"Sorry, {selected_product.name} is out of stock.")
        else:
            print("\nInvalid input. Please try again.")