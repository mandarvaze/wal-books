from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .models import Book
from .views import IndexView


class BookIndexViewTests(TestCase):
    def test_authenticated_access(self):
        """
        User needs to login, in order to view the list of books
        """
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 302)
        assert "login" in response.url

    def test_no_books(self):
        factory = RequestFactory()
        request = factory.get("/books/")
        request.user = AnonymousUser()
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        assert "books" in response.context_data
        assert response.context_data["books"].count() == 0

    def test_books(self):
        book_name = "TDD with Django"
        book = Book(name=book_name)
        book.save()

        factory = RequestFactory()
        request = factory.get("/books/")
        request.user = AnonymousUser()
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        assert "books" in response.context_data
        assert response.context_data["books"].count() == 1
        assert response.context_data["books"].get().name == book_name
