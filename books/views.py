from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from decimal import Decimal

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    
    # Sorting
    sort_by = request.GET.get('sort', 'title')
    if sort_by in ['title', 'author', 'published_year']:
        books = books.order_by(sort_by)
    
    # Filter by genre (Sprint 3)
    genre = request.GET.get('genre')
    if genre:
        books = books.filter(genre__iexact=genre)

    # Filter by rating (Sprint 4)
    rating = request.GET.get('rating')
    if rating:
        books = books.filter(rating__gte=rating)

    book_data = []
    for book in books:
        book_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'isbn': book.isbn,
            'published_year': book.published_year,
            'genre': book.genre,
            'copies_sold': book.copies_sold,
            'rating': book.rating,
            'publisher': book.publisher,
            'price': book.price,
        })
    
    return Response(book_data)

@api_view(['GET'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)
    
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'isbn': book.isbn,
        'published_year': book.published_year,
        'genre': book.genre,
        'copies_sold': book.copies_sold,
        'rating': book.rating,
        'publisher': book.publisher,
        'price': book.price,
    }
    
    return Response(book_data)

@api_view(['GET'])
def top_sellers(request):
    books = Book.objects.all().order_by('-copies_sold')[:10]
    
    book_data = []
    for book in books:
        book_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'isbn': book.isbn,
            'published_year': book.published_year,
            'genre': book.genre,
            'copies_sold': book.copies_sold,
            'rating': book.rating,
            'publisher': book.publisher,
            'price': book.price,
        })
    
    return Response(book_data)

@api_view(['PATCH'])
def discount_by_publisher(request):
    publisher = request.data.get('publisher')
    discount_percent = request.data.get('discount_percent')

    if not publisher or discount_percent is None:
        return Response({'error': 'publisher and discount_percent are required'}, status=400)

    try:
        discount_percent = Decimal(str(discount_percent))
    except:
        return Response({'error': 'Invalid discount_percent'}, status=400)

    if discount_percent < 0 or discount_percent > 100:
        return Response({'error': 'discount_percent must be between 0 and 100'}, status=400)

    books = Book.objects.filter(publisher__iexact=publisher)

    if not books.exists():
        return Response({'error': 'No books found for this publisher'}, status=404)

    for book in books:
        book.price = book.price * (1 - discount_percent / 100)
        book.save()

    return Response({'message': f'Discount applied to {books.count()} books by {publisher}'})