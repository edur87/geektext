from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wishlist, WishlistItem
from .serializers import (
    WishlistSerializer,
    WishlistItemSerializer,
    WishlistItemCreateSerializer,
)


class WishlistListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        return Response(WishlistSerializer(wishlists, many=True).data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wishlist = Wishlist.objects.create(
            user=request.user,
            name=serializer.validated_data["name"],
        )

        return Response(
            WishlistSerializer(wishlist).data,
            status=status.HTTP_201_CREATED,
        )


class WishlistItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_wishlist(self, request, wishlist_id):
        return get_object_or_404(
            Wishlist,
            id=wishlist_id,
            user=request.user,
        )

    def get(self, request, wishlist_id):
        wishlist = self.get_wishlist(request, wishlist_id)
        items = WishlistItem.objects.filter(wishlist=wishlist)
        return Response(WishlistItemSerializer(items, many=True).data)

    def post(self, request, wishlist_id):
        wishlist = self.get_wishlist(request, wishlist_id)

        serializer = WishlistItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]

        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            book_id=book_id,
        )

        if not created:
            return Response(
                {"detail": "Book already in wishlist."},
                status=status.HTTP_200_OK,
            )

        return Response(
            WishlistItemSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )


class WishlistItemDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, wishlist_id, book_id):
        wishlist = get_object_or_404(
            Wishlist,
            id=wishlist_id,
            user=request.user,
        )

        item = WishlistItem.objects.filter(
            wishlist=wishlist,
            book_id=book_id,
        ).first()

        if not item:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
