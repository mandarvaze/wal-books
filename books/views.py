from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView

from .forms import NewAuthorForm, NewBookForm
from .models import Author, Book


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = ", ".join([str(author) for author in book.authors.all()])
    genres = ", ".join([str(genre) for genre in book.genres.all()])
    return render(
        request,
        "books/detail.html",
        {"name": book.name, "authors": authors, "genres": genres},
    )


def new_book(request):
    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/books/")
    else:
        form = NewBookForm()
    return render(request, "books/new_book.html", {"form": form})


class BookList(ListView):
    model = Book


class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("book_list")


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("book_list")


def author_book_names(request):
    without_books = Author.objects.filter(book__isnull=True).all()
    with_books = Author.objects.exclude(book__isnull=True).all()
    return render(
        request,
        "authors/index.html",
        {"with_books": with_books, "without_books": without_books},
    )


def new_author(request):
    if request.method == "POST":
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/authors/")
    else:
        form = NewAuthorForm()
    return render(request, "books/new_author.html", {"form": form})
