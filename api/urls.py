from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import health

urlpatterns = [
    path("health/", health),
    path("token/", obtain_auth_token),

]