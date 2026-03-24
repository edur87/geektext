from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


def _wants_json(request):
    accept_header = request.headers.get("Accept", "")
    return request.GET.get("format") == "json" or (
        "application/json" in accept_header and "text/html" not in accept_header
    )


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

    if not _wants_json(request):
        return render(
            request,
            "books/book_list.html",
            {
                "books": books,
                "active_sort": sort_by,
                "active_genre": genre or "",
            },
        )

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

    return JsonResponse(book_data, safe=False)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not _wants_json(request):
        return render(request, "books/book_detail.html", {"book": book})

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

    return JsonResponse(book_data)


def top_sellers(request):
    books = Book.objects.all().order_by('-copies_sold')[:10]

    if not _wants_json(request):
        return render(
            request,
            "books/book_list.html",
            {
                "books": books,
                "active_sort": "-copies_sold",
                "active_genre": "",
                "page_title": "Top Sellers",
            },
        )

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

    return JsonResponse(book_data, safe=False)


# REST API Endpoints

class BookCreateListView(APIView):
    """
    POST: Create a new book
    GET: List all books or filter by author
    """
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # List all books with optional filters
        books = Book.objects.all()
        
        # Filter by author_id
        author_id = request.query_params.get('author_id')
        if author_id:
            books = books.filter(author_id=author_id)
        
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookRetrieveView(APIView):
    """
    GET: Retrieve a book by ID or ISBN
    """
    
    def get(self, request, pk):
        # Try to find by ID first, then by ISBN
        book = None
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            book = get_object_or_404(Book, isbn=pk)
        
        serializer = BookSerializer(book)
        return Response(serializer.data)


class AuthorCreateListView(APIView):
    """
    POST: Create a new author
    GET: List all authors
    """
    
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class AuthorBooksView(APIView):
    """
    GET: Retrieve all books by a specific author
    """
    
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)