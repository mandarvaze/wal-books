from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .models import Author, Book
from .views import AuthorsIndexView, IndexView


class HomeTests(TestCase):
    def test_home_redirects(self):
        """
        "/" redirects to "/books"
        """
        response = self.client.get("/")
        self.assertRedirects(
            response, "/books/", status_code=301, target_status_code=302
        )


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


class AuthorIndexViewTests(TestCase):
    def test_authenticated_access(self):
        """
        User needs to login, in order to view the list of authors
        """
        response = self.client.get("/authors/")
        self.assertEqual(response.status_code, 302)
        assert "login" in response.url

    def test_no_authors(self):
        factory = RequestFactory()
        request = factory.get("/authors/")
        request.user = AnonymousUser()
        response = AuthorsIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        assert "authors" in response.context_data
        assert response.context_data["authors"].count() == 0

    def test_authors(self):
        author_fname = "Daniel"
        author_lname = "Roy Greenfeld"
        author = Author(first_name=author_fname, last_name=author_lname)
        author.save()

        factory = RequestFactory()
        request = factory.get("/authors/")
        request.user = AnonymousUser()
        response = AuthorsIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        assert "authors" in response.context_data
        assert response.context_data["authors"].count() == 1
        assert response.context_data["authors"].get().first_name == author_fname
        assert response.context_data["authors"].get().last_name == author_lname
