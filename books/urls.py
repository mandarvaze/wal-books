from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("<int:book_id>/", login_required(views.detail), name="detail"),
]
