from django.urls import path
from .views import (
    WishlistListCreateView,
    WishlistItemsView,
    WishlistItemDeleteView,
    WishlistItemMoveToCartView,
    WishlistDeleteView,
)

urlpatterns = [
    path("wishlists/", WishlistListCreateView.as_view()),
    path("wishlists/<int:wishlist_id>/items/", WishlistItemsView.as_view()),
    path(
        "wishlists/<int:wishlist_id>/items/<int:book_id>/",
        WishlistItemDeleteView.as_view(),
    ),
    path(
        "wishlists/<int:wishlist_id>/items/<int:book_id>/move-to-cart/",
        WishlistItemMoveToCartView.as_view(),
    ),
    path(
        "wishlists/<int:wishlist_id>/",
        WishlistDeleteView.as_view(),
    ),
]