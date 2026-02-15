from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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
            return Response({"error": "book_id and user_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, id=book_id)

        cart_item, created = ShoppingCart.objects.get_or_create(user_id=user_id, book=book)

        if not created:
            pass

        return Response({"message": "Book added to cart"}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        #delete a book from shopping cart Parameters sent: Book Id, User Id
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')

        cart_item = get_object_or_404(ShoppingCart, user_id=user_id, book_id=book_id)
        cart_item.delete()

        return Response({"message": "Book removed from cart"}, status=status.HTTP_200_OK)
    
#retrieve list
class CartListView(APIView):
    def get(self, request, user_id):

        items = ShoppingCart.objects.filter(user_id=user_id)
        serialzer = ShoppingCartSerializer(items, many=True)
        return Response(serialzer.data, status=status.HTTP_200_OK)


class CartSubtotalView(APIView):
    def get(self, request, user_id):
        #retrieve the subtotal price of items in the user's shopping cart
        items = ShoppingCart.objects.filter(user_id=user_id)

        total = sum(item.book.price for item in items)

        return Response({"subtotal": total}, status=status.HTTP_200_OK)