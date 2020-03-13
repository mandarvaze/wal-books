from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.author_book_names), name="authors_index"),
    path("new/", login_required(views.new_author), name="new_author"),
]
