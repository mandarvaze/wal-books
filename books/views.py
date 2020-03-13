from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Book


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = ", ".join([str(author) for author in book.authors.all()])
    genres = ", ".join([str(genre) for genre in book.genres.all()])
    return render(
        request,
        "books/detail.html",
        {"name": book.name, "authors": authors, "genres": genres},
    )


class IndexView(generic.ListView):
    template_name = "books/index.html"
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.all()
