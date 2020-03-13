from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("<int:book_id>/", login_required(views.detail), name="detail"),
    path("new/", login_required(views.new_book), name="new_book"),
]
