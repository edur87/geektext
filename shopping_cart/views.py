from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import ShoppingCart, Book
from .serializers import ShoppingCartSerializer

class ManageCartView(APIView):
    def post(self, request):
        """
        Adds a book to the shopping cart, parameters sent: Book Id, User Id
        """
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')

        #validating
        if not book_id or not user_id:
            return Response(
                {"error": "book_id and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, id=book_id)
        user = get_object_or_404(User, id=user_id)

        cart_item, created = ShoppingCart.objects.get_or_create(user=user, book=book)

        if not created:
            cart_item.refresh_from_db()
            cart_item.quantity += 1
            cart_item.save()
            return Response({"message": "Book quantity updated in cart"}, status=status.HTTP_200_OK)

        return Response({"message": "Book added to cart"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        #delete a book from shopping cart Parameters sent: Book Id, User Id
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')

        if not book_id or not user_id:
            return Response(
                {"error": "book_id and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(ShoppingCart, user_id=user_id, book_id=book_id)
        cart_item.delete()

        return Response({"message": "Book removed from cart"}, status=status.HTTP_200_OK)
    
#retrieve list
class CartListView(APIView):
    def get(self, request, user_id):
        get_object_or_404(User, id=user_id) #validate user
        items = ShoppingCart.objects.filter(user_id=user_id)
        serializer = ShoppingCartSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartSubtotalView(APIView):
    def get(self, request, user_id):
        get_object_or_404(User, id=user_id) #validate user
        #retrieve the subtotal price of items in the user's shopping cart
        items = ShoppingCart.objects.filter(user_id=user_id)

        try:
            total = sum(item.book.price * item.quantity for item in items)
        except AttributeError:
            return Response(
                {"error": "Price data is not available"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({"subtotal": total}, status=status.HTTP_200_OK)