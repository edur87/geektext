from django.urls import path
from . import views

urlpatterns = [
    path("books/<int:book_id>/comments/", views.api_add_comment, name="api_add_comment"),
]

  