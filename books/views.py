from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Book


def index(request):
    books = Book.objects.all()
    template = loader.get_template("books/index.html")
    context = {
        "books": books,
    }
    return HttpResponse(template.render(context, request))


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = ", ".join([str(author) for author in book.authors.all()])
    genres = ", ".join([str(genre) for genre in book.genres.all()])
    return render(
        request,
        "books/detail.html",
        {"name": book.name, "authors": authors, "genres": genres},
    )
