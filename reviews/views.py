from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Comment, Review
from .serializers import ReviewSerializer
from books.models import Book


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def api_add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "GET":
        qs = (
            Comment.objects
            .filter(book=book)
            .select_related("user")
            .order_by("-created_at")
        )
        data = [
            {
                "id": c.id,
                "book_id": book.id,
                "user_id": c.user_id,
                "username": c.user.username if c.user_id else None,
                "comment": c.comment,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in qs
        ]
        return Response(data, status=status.HTTP_200_OK)

    text = (request.data.get("comment") or "").strip()
    if not text:
        return Response(
            {"error": "comment is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    c = Comment.objects.create(book=book, user=request.user, comment=text)
    return Response(
        {
            "id": c.id,
            "book_id": book.id,
            "user_id": request.user.id,
            "username": request.user.username,
            "comment": c.comment,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request):
    serializer = ReviewSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(
            {
                "message": "Review created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)