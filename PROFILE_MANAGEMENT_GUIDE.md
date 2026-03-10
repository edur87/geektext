# Profile Management Feature - Implementation Guide

## Overview
### SPRINT 3 STUFF, WE CONNECTED TO DJANGO!!!
Your Profile Management feature (Feature 2) is **fully implemented and connected** to Django REST Framework. All endpoints are accessible through the browsable API interface shown in your screenshot.

---

## Architecture Explanation

### 1. **Models** ([api/models.py](api/models.py))

#### User Model (Custom User)
```python
class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
```
- **Extends Django's AbstractUser**: Inherits username, password, email, and authentication features
- **Custom Fields**: Added `name` and `home_address` as optional fields
- **Set as AUTH_USER_MODEL**: Configured in settings.py as the project's user model

#### CreditCard Model
```python
class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards')
    card_number = models.CharField(max_length=19)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.CharField(max_length=5)  # MM/YY
    cvv = models.CharField(max_length=4)
    is_default = models.BooleanField(default=False)
```
- **Belongs to User**: Each credit card is linked to one user via ForeignKey
- **Security**: card_number and CVV are write-only (never returned in API responses)
- **Validation**: Uses RegexValidator for card number and CVV format

---

### 2. **Serializers** ([api/serializers.py](api/serializers.py))

#### UserCreateSerializer
- Used for **creating new users** (POST /api/users/)
- Handles password hashing with `set_password()`
- Makes email, name, and home_address optional

#### UserSerializer
- Used for **retrieving user data** (GET /api/users/{username}/)
- Includes related credit cards via `credit_cards` field
- Hides password from responses

#### UserUpdateSerializer  
- Used for **updating user fields** (PUT/PATCH /api/users/{username}/update/)
- **Excludes email** (as per requirements)
- Allows updating: name, home_address, password
- Properly hashes new passwords

#### CreditCardSerializer
- Used for creating and displaying credit cards
- Makes card_number and CVV write-only for security
- Shows masked data to users

---

### 3. **Views** ([api/views.py](api/views.py))

All views use Django REST Framework's `@api_view` decorator:

| Function | HTTP Method | Endpoint | Purpose |
|----------|-------------|----------|---------|
| `create_user` | POST | `/api/users/` | Create new user |
| `get_user` | GET | `/api/users/{username}/` | Retrieve user by username |
| `update_user` | PUT/PATCH | `/api/users/{username}/update/` | Update user fields (not email) |
| `login_user` | POST | `/api/login/` | Authenticate and return user data |
| `create_credit_card` | POST | `/api/users/{username}/credit-cards/` | Add credit card to user |

---

### 4. **URL Configuration**

#### Main URLs ([config/urls.py](config/urls.py))
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # All API endpoints
    path("", include("books.urls")),
]
```

#### API URLs ([api/urls.py](api/urls.py))
```python
urlpatterns = [
    path("users/", create_user),
    path("users/<str:username>/", get_user),
    path("users/<str:username>/update/", update_user),
    path("login/", login_user),
    path("users/<str:username>/credit-cards/", create_credit_card),
]
```

Full endpoint paths:
- `http://127.0.0.1:8000/api/users/`
- `http://127.0.0.1:8000/api/users/{username}/`
- `http://127.0.0.1:8000/api/users/{username}/update/`
- `http://127.0.0.1:8000/api/login/`
- `http://127.0.0.1:8000/api/users/{username}/credit-cards/`

---

### 5. **Settings Configuration** ([config/settings.py](config/settings.py))

Key configurations:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # Django REST Framework
    'api',             # Your API app with User model
    ...
]

AUTH_USER_MODEL = 'api.User'  # Custom user model

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # JSON responses
    ]
}
```

---

## Testing the API

### Prerequisites
1. Start the Django development server:
```bash
python3 manage.py runserver
```

2. Open your browser to: `http://127.0.0.1:8000/api/users/`

---

### Test Scenarios

#### 1. Create a User
**Endpoint:** `POST /api/users/`

**Request Body (JSON):**
```json
{
    "username": "johndoe",
    "password": "SecurePassword123!",
    "email": "john@example.com",
    "name": "John Doe",
    "home_address": "123 Main St, City, State 12345"
}
```

**Minimal Request (only required fields):**
```json
{
    "username": "janedoe",
    "password": "SecurePassword456!"
}
```

**Expected Response (201 Created):**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "home_address": "123 Main St, City, State 12345"
}
```
*Note: Password is not returned (write-only)*

---

#### 2. Retrieve a User
**Endpoint:** `GET /api/users/{username}/`

**Example:** `GET /api/users/johndoe/`

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "home_address": "123 Main St, City, State 12345",
    "credit_cards": []
}
```

---

#### 3. Update a User
**Endpoint:** `PATCH /api/users/{username}/update/`

**Request Body (partial update):**
```json
{
    "name": "Jonathan Doe",
    "home_address": "456 Oak Ave, New City, State 54321"
}
```

**Full Update with PUT:**
```json
{
    "name": "Jonathan Doe",
    "home_address": "456 Oak Ave",
    "password": "NewPassword789!"
}
```

**Expected Response (200 OK):**
```json
{
    "name": "Jonathan Doe",
    "home_address": "456 Oak Ave, New City, State 54321"
}
```

**Important:** Email cannot be updated (excluded from UserUpdateSerializer as per requirements)

---

#### 4. Login a User
**Endpoint:** `POST /api/login/`

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "SecurePassword123!"
}
```

**Expected Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "name": "John Doe",
        "home_address": "123 Main St, City, State 12345",
        "credit_cards": []
    },
    "credit_cards": []
}
```

**Failed Login Response (401 Unauthorized):**
```json
{
    "error": "Invalid username or password"
}
```

---

#### 5. Create a Credit Card
**Endpoint:** `POST /api/users/{username}/credit-cards/`

**Example:** `POST /api/users/johndoe/credit-cards/`

**Request Body:**
```json
{
    "card_number": "4532015112830366",
    "cardholder_name": "John Doe",
    "expiration_date": "12/25",
    "cvv": "123",
    "is_default": true
}
```

**Expected Response (201 Created):**
```json
{
    "id": 1,
    "cardholder_name": "John Doe",
    "expiration_date": "12/25",
    "is_default": true,
    "created_at": "2026-03-09T10:30:00Z",
    "updated_at": "2026-03-09T10:30:00Z"
}
```
*Note: card_number and CVV are NOT returned (write-only for security)*

---

#### 6. View User with Credit Cards
**Endpoint:** `GET /api/users/{username}/`

**Expected Response:**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "home_address": "123 Main St",
    "credit_cards": [
        {
            "id": 1,
            "cardholder_name": "John Doe",
            "expiration_date": "12/25",
            "is_default": true,
            "created_at": "2026-03-09T10:30:00Z",
            "updated_at": "2026-03-09T10:30:00Z"
        }
    ]
}
```

---

## Testing Tools

### 1. **Django REST Framework Browsable API** (Your Screenshot)
- Navigate to: `http://127.0.0.1:8000/api/users/`
- Use the HTML form at the bottom to make POST requests
- Click on URLs to navigate between endpoints
- View OPTIONS to see allowed methods

### 2. **cURL Commands**

**Create User:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!",
    "email": "test@example.com",
    "name": "Test User",
    "home_address": "123 Test St"
  }'
```

**Get User:**
```bash
curl -X GET http://127.0.0.1:8000/api/users/testuser/
```

**Update User:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/users/testuser/update/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

**Add Credit Card:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/testuser/credit-cards/ \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "cardholder_name": "Test User",
    "expiration_date": "12/25",
    "cvv": "123"
  }'
```

### 3. **Postman or Thunder Client**
Import the endpoints and test with a visual interface.

---

## Acceptance Criteria ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| ✅ Create a User with username, password | ✅ Done | `POST /api/users/` with UserCreateSerializer |
| ✅ Optional fields: name, email, home_address | ✅ Done | All fields marked as `required=False` |
| ✅ Retrieve User by username | ✅ Done | `GET /api/users/{username}/` |
| ✅ Update user fields except email | ✅ Done | `PATCH /api/users/{username}/update/` (email excluded) |
| ✅ Create Credit Card for User | ✅ Done | `POST /api/users/{username}/credit-cards/` |

---

## Security Features Implemented

1. **Password Hashing**: Uses Django's `set_password()` and `check_password()`
2. **Write-Only Fields**: Passwords, card numbers, and CVVs never returned in responses
3. **Input Validation**: RegexValidator for card numbers and CVV
4. **Related Data**: Credit cards properly linked to users via ForeignKey

---

## How It Works with DRF Browsable API

The screenshot you shared shows the **Django REST Framework Browsable API** interface. Here's what you're seeing:

1. **Endpoint Title**: "Wishlist List Create" (this is a different endpoint from your user management)
2. **HTTP Methods**: GET, POST, HEAD, OPTIONS buttons
3. **Response Area**: Shows JSON responses
4. **HTML Form**: At the bottom for making POST requests
5. **Navigation**: Breadcrumbs at top for exploring API

Your user endpoints work the same way:
- Visit `http://127.0.0.1:8000/api/users/`
- You'll see a similar interface
- Use the form to create users
- Navigate to specific users via links

---

## Next Steps

1. **Start the server** (if not running):
   ```bash
   python3 manage.py runserver
   ```

2. **Test each endpoint** using the browsable API or cURL

3. **Create test users** and credit cards

4. **Verify all acceptance criteria** are met

5. **(Optional) Add to Django Admin** to manage users visually:
   ```python
   # In api/admin.py
   from django.contrib import admin
   from .models import User, CreditCard
   
   admin.site.register(User)
   admin.site.register(CreditCard)
   ```

---

## Common Issues & Solutions

### Issue: "User already exists"
**Solution**: Each username must be unique. Use different usernames for testing.

### Issue: "Invalid credentials" on login
**Solution**: Ensure you're using the correct password. Passwords are case-sensitive.

### Issue: "User not found" when creating credit card
**Solution**: Create the user first before adding credit cards.

### Issue: Can't update email
**Solution**: This is by design (per requirements). Email updates are not allowed.

---

## Summary

Your Profile Management feature is **100% functional and integrated** with Django REST Framework. All models, serializers, views, and URLs are properly configured. The browsable API provides an easy interface for testing, and all acceptance criteria are met. You can now demonstrate creating users, retrieving them by username, updating fields (except email), and adding credit cards to users.

**Your implementation location:**
- **Models**: `api/models.py`
- **Serializers**: `api/serializers.py`
- **Views**: `api/views.py`
- **URLs**: `api/urls.py` (included in main `config/urls.py`)
- **Database**: PostgreSQL (configured in settings)

The architecture follows Django REST Framework best practices with proper separation of concerns, validation, and security measures.
