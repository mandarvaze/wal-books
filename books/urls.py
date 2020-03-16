from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("<int:book_id>/", login_required(views.detail), name="book_view"),
    path("new/", login_required(views.new_book), name="new_book"),
    path("", login_required(views.BookList.as_view()), name="book_list"),
    path("edit/<int:pk>", login_required(views.BookUpdate.as_view()), name="book_edit"),
    path(
        "delete/<int:pk>",
        login_required(views.BookDelete.as_view()),
        name="book_delete",
    ),
]
