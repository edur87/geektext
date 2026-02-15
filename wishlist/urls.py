from django.urls import path
from .views import (
    WishlistListCreateView,
    WishlistItemsView,
    WishlistItemDeleteView,
)

urlpatterns = [
    path("wishlists/", WishlistListCreateView.as_view()),
    path("wishlists/<int:wishlist_id>/items/", WishlistItemsView.as_view()),
    path(
        "wishlists/<int:wishlist_id>/items/<int:book_id>/",
        WishlistItemDeleteView.as_view(),
    ),
]
