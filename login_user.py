#!/usr/bin/env python3
"""
User Login Script
Prompts for username and password, and displays user profile information
"""

import requests
import json
from tabulate import tabulate

API_URL = "http://localhost:8000/api"

def print_header(title):
    """Print a formatted header"""
    print ("\n" + "="*60)
    print (f"  {title}")
    print ("="*60)

def login ():
    """Prompt for credentials and authenticate user"""
    print_header ("User Login")
    
    username = input ("Username: ").strip()
    if not username:
        print ("\nError: Username is required")
        return None
    
    password = input ("Password: ").strip()
    
    if not password:
        print ("\nError: Password is required")
        return None
    
    try:
        response = requests.post(
            f"{API_URL}/login/",
            json={"username": username, "password": password},
            timeout=5
        )
        
        if response.status_code == 200:
            # Try to decode JSON response. If decoding fails, show raw response for debugging.
            try:
                return response.json()
            except Exception:
                print ("\nError: Received non-JSON response from server (debug output):")
                print (response.text or '<empty response>')
                return None
        elif response.status_code == 401:
            print ("\nError: Invalid username or password")
            return None
        else:
            # Try extracting error message from JSON, otherwise show raw text
            try:
                err = response.json().get('error', 'Unknown error')
            except Exception:
                err = response.text or 'Unknown error (non-JSON response)'
            print (f"\nError: {err}")
            return None
            
    except requests.exceptions.ConnectionError:
        print ("\nError: Cannot connect to server. Make sure the server is running!")
        print ("   Run: python3 manage.py runserver --settings=config.settings_test")
        return None
    except Exception as e:
        print (f"\nError: {str(e)}")
        return None

def display_user_info (user_data):
    """Display user information in a formatted table"""
    print_header ("User Profile Information")
    
    # Basic user info
    basic_info = [
        ["ID:", user_data.get('id', 'N/A')],
        ["Username:", user_data.get('username', 'N/A')],
        ["Email:", user_data.get('email', 'N/A')],
        ["Full Name:", user_data.get('name', 'N/A')],
        ["Home Address:", user_data.get('home_address', 'N/A')],
    ]
    
    print ("\nAccount Details:")
    print (tabulate(basic_info, headers=["Field:", "Value:"], tablefmt="simple"))
    
    # Credit cards info
    credit_cards = user_data.get('credit_cards', [])
    if credit_cards:
        print ("\nSaved Credit Cards:")
        cards_info = []
        for idx, card in enumerate(credit_cards, 1):
            cards_info.append([
                idx,
                card.get('cardholder_name', 'N/A'),
                f"****{card.get('expiration_date', 'N/A').split('/')[-1]}",  # Last 2 digits of expiration
                "Yes" if card.get('is_default') else "No",
            ])
        print (tabulate(cards_info, headers=["#", "Cardholder:", "Exp:", "Default:"], tablefmt="simple"))
    else:
        print ("\nNo saved credit cards")

def main ():
    """Main function"""
    print ("\n" + "="*60)
    print ("Welcome to GeekText User Portal")
    print ("="*60)
    
    user_data = login()
    
    if user_data:
        display_user_info(user_data)
        print ("\nLogin successful!\n")
    else:
        print ("\nLogin failed. Please try again.\n")

if __name__ == "__main__":
    main()
