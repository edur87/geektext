from django.urls import path
from . import views

urlpatterns = [
    path('users/create/', views.create_user, name='create_user'),
    path('users/<str:username>/', views.get_user, name='get_user'),
    path('users/<str:username>/update/', views.update_user, name='update_user'),
    path('login/', views.login_user, name='login_user'),
    path('users/<str:username>/credit-cards/', views.create_credit_card, name='create_credit_card'),
]
