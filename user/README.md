# User Management Module

This folder contains all user profile and credit card management functionality for the GeekText application.

## Files Overview

### Core Django App Files
- **`__init__.py`** - Python package initialization
- **`apps.py`** - Django app configuration
- **`models.py`** - Database models for User and CreditCard
- **`views.py`** - API views for user operations
- **`serializers.py`** - DRF serializers for User and CreditCard
- **`admin.py`** - Django admin interface configuration
- **`urls.py`** - API endpoint routing

### Demo/Testing Scripts
- **`demo.py`** - Interactive demo for complete profile management workflow
  - Create new user
  - Retrieve user profile
  - Update user information
  - Add credit cards
  - Login and verify complete profile

- **`login_user.py`** - User login and profile viewing script
  - Login with username/password
  - Display user profile information
  - Show saved credit cards

### Database
- **`migrations/`** - Django migration files for schema changes

## API Endpoints

All endpoints are prefixed with `/api/`:

- `POST /users/create/` - Create a new user
- `GET /users/<username>/` - Get user profile
- `PUT /users/<username>/update/` - Update user profile
- `PATCH /users/<username>/update/` - Partially update user profile
- `POST /login/` - Login user
- `POST /users/<username>/credit-cards/` - Add credit card

## Usage

### Running Demo
```bash
python user/demo.py
```

### Running Login Script
```bash
python user/login_user.py
```

## Models

### User
Extended Django User model with:
- `name` - Full name
- `home_address` - Home address
- Relationship to CreditCard (one-to-many)

### CreditCard
- `user` - ForeignKey to User
- `card_number` - 13-19 digit card number
- `cardholder_name` - Name on card
- `expiration_date` - MM/YY format
- `cvv` - 3-4 digit security code
- `is_default` - Default payment method flag
- `created_at` - Timestamp
- `updated_at` - Timestamp
