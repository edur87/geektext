from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Book


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