#!/usr/bin/env python3
"""
User Profile Management System Demo
Interactive demo for the complete profile management workflow
"""

import requests
import json
from tabulate import tabulate

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def get_user_input(prompt, required=True):
    """Get input from user with validation"""
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("This field is required. Please try again.\n")
            continue
        return value

def demo():
    print_header("USER PROFILE")
    
    # 1. create user.
    print_header ("Create New User")
    print("Please enter the following information to create a new account:\n")
    
    user_data = {
        "username": get_user_input ("Username: "),
        "password": get_user_input ("Password: "),
        "name": get_user_input ("Full name: "),
        "home_address": get_user_input ("Home address: "),
    }
    
    print("\nCreating user with the following profile information:")
    table_data = [
        ["Username", user_data["username"]],
        ["Name", user_data["name"]],
        ["Address", user_data["home_address"]],
    ]
    print (tabulate (table_data, headers=["Field", "Value"], tablefmt="simple"))
    print ()
    
    try:
        response = requests.post (f"{BASE_URL}/api/users/", json=user_data)
        if response.status_code == 201:
            created_user = response.json ()
            print("Status: User created successfully!")
            print(f"User ID: {created_user.get('id')}")
            print(f"Date Joined: {created_user.get('date_joined')}\n")
        else:
            print(f"Error: {response.status_code}")
            print (f"Details: {response.json ()}\n")
            return
    except Exception as e:
        print (f"Error: {e}\n")
        return
    
    # 2. retrieve user.
    print_header ("Retrieve User Profile")
    username = user_data["username"]
    print(f"Fetching profile for user: {username}\n")
    
    try:
        response = requests.get (f"{BASE_URL}/api/users/{username}/")
        if response.status_code == 200:
            profile = response.json ()
            table_data = [
                ["Username", profile.get ("username")],
                ["Name", profile.get ("name")],
                ["Address", profile.get ("home_address")],
                ["Member Since", profile.get ("date_joined")],
            ]
            print("User Profile Retrieved:")
            print(tabulate(table_data, headers=["Field", "Value"], tablefmt="simple"))
            print()
        else:
            print(f"Error: {response.status_code}\n")
            return
    except Exception as e:
        print(f"Error: {e}\n")
        return
    
    # 3. update user.
    print_header ("Update User Profile")
    print("Would you like to update your profile information? (yes/no): ", end="")
    if input().strip().lower() in ['yes', 'y']:
        update_data = {
            "name": get_user_input("New name (press Enter to skip): ", required=False) or user_data["name"],
            "home_address": get_user_input("New address (press Enter to skip): ", required=False) or user_data["home_address"],
        }
        
        if update_data["name"] != user_data["name"] or update_data["home_address"] != user_data["home_address"]:
            print("\nUpdating user information:")
            table_data = [
                ["Name", update_data["name"]],
                ["Address", update_data["home_address"]],
            ]
            print(tabulate(table_data, headers=["Field", "New Value"], tablefmt="simple"))
            print()
            
            try:
                response = requests.put(f"{BASE_URL}/api/users/{username}/update/", json=update_data)
                if response.status_code == 200:
                    updated = response.json()
                    print("Status: Profile updated successfully!")
                    print(f"Name: {updated.get('name')}")
                    print(f"Address: {updated.get('home_address')}\n")
                else:
                    print(f"Error: {response.status_code}\n")
            except Exception as e:
                print(f"Error: {e}\n")
        else:
            print("No changes made.\n")
    else:
        print("Skipping profile update.\n")
    
    # 4. add credit cards.
    print_header ("Add Credit Cards")
    print("Would you like to add credit cards to your account? (yes/no): ", end="")
    
    card_count = 0
    if input().strip().lower() in ['yes', 'y']:
        while True:
            print(f"\nEnter credit card {card_count + 1} information:\n")
            card_data = {
                "card_number": get_user_input("Card number (13-19 digits): "),
                "cardholder_name": get_user_input("Cardholder name: "),
                "expiration_date": get_user_input("Expiration date (MM/YYYY): "),
                "cvv": get_user_input("CVV (3-4 digits): "),
            }
            
            print("\nAdding credit card:")
            table_data = [
                ["Cardholder", card_data["cardholder_name"]],
                ["Card Number", f"****{card_data['card_number'][-4:]}"],
                ["Expiration", card_data["expiration_date"]],
            ]
            print(tabulate(table_data, headers=["Field", "Value"], tablefmt="simple"))
            print()
            
            try:
                response = requests.post(f"{BASE_URL}/api/users/{username}/credit-cards/", json=card_data)
                if response.status_code == 201:
                    card = response.json()
                    card_count += 1
                    print("Status: Credit card added successfully!")
                    print(f"Card ID: {card.get('id')}")
                    print(f"Added: {card.get('created_at')}\n")
                else:
                    print(f"Error: {response.status_code}")
                    print(f"Details: {response.json()}\n")
            except Exception as e:
                print(f"Error: {e}\n")
            
            print("Would you like to add another card? (yes/no): ", end="")
            if input().strip().lower() not in ['yes', 'y']:
                break
    else:
        print("Skipping credit card setup.\n")
    
    # 5. login and retrieve complete profile.
    print_header ("Login and Retrieve Complete Profile")
    print("Now let's verify everything by logging in to your account.\n")
    print("Logging in with credentials:")
    print(f"Username: {username}")
    print(f"Password: (hidden)\n")
    
    login_data = {
        "username": username,
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print("Status: Login successful!\n")
            
            # display user info.
            user = login_result.get ("user", {})
            print("User Information:")
            user_table = [
                ["Username", user.get("username")],
                ["Name", user.get("name")],
                ["Address", user.get("home_address")],
            ]
            print(tabulate(user_table, headers=["Field", "Value"], tablefmt="simple"))
            print()
            
            # display credit cards.
            cards = login_result.get ("credit_cards", [])
            if cards:
                print(f"Credit Cards on File ({len(cards)}):")
                cards_table = []
                for i, card in enumerate(cards, 1):
                    cards_table.append([
                        i,
                        f"****{card.get('card_number', '')[-4:]}",
                        card.get("cardholder_name"),
                        card.get("expiration_date"),
                        card.get("created_at", "")[:10]
                    ])
                print(tabulate(cards_table, headers=["ID", "Card Number", "Cardholder", "Expiration", "Added"], tablefmt="simple"))
                print()
            else:
                print("No credit cards on file.\n")
        else:
            print(f"Error: {response.status_code}")
            print(f"Details: {response.json()}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # demo complete.
    print_header ("DEMO COMPLETE")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server at http://localhost:8000")
        print("Make sure the Django server is running:")
        print("  python3 manage.py runserver")
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
