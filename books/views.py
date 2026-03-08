from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book

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
        })
    
    return Response(book_data)