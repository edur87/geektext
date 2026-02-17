from django.urls import path
from .views import health, create_user, get_user, update_user, create_credit_card, login_user

urlpatterns = [
    path("health/", health),
    
    # Profile Management - User endpoints
    path("users/", create_user, name="create_user"),
    path("users/<str:username>/", get_user, name="get_user"),
    path("users/<str:username>/update/", update_user, name="update_user"),
    path("login/", login_user, name="login_user"),
    
    # Profile Management - Credit Card endpoints
    path("users/<str:username>/credit-cards/", create_credit_card, name="create_credit_card"),
]