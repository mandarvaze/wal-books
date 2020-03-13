from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .models import Author, Book
from .views import IndexView, author_book_names, new_author, new_book


class HomeTests(TestCase):
    def test_home_redirects(self):
        """
        "/" redirects to "/books"
        """
        response = self.client.get("/")
        self.assertRedirects(
            response, "/books/", status_code=301, target_status_code=302
        )


class SignupTests(TestCase):
    def test_signup(self):
        response = self.client.get("/signup/")
        html = str(response.content)
        assert response.status_code == 200
        fields = ["Username:", "Password:", "Password confirmation:"]
        for fld in fields:
            assert fld in html


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
        response = author_book_names(request)
        self.assertEqual(response.status_code, 200)
        assert "Authors with" not in str(response.content)

    def test_authors(self):
        author_fname = "Daniel"
        author_lname = "Roy Greenfeld"
        author = Author(first_name=author_fname, last_name=author_lname)
        author.save()

        factory = RequestFactory()
        request = factory.get("/authors/")
        request.user = AnonymousUser()
        response = author_book_names(request)
        self.assertEqual(response.status_code, 200)
        assert "<h1>Authors with at least</h1>" not in str(response.content)
        assert "<h1>Authors without any Books</h1>" in str(response.content)
        assert f"{author_fname} {author_lname}" in str(response.content)


class NewBookTests(TestCase):
    def test_authenticated_access(self):
        """
        User needs to login, in order to add a new book
        """
        response = self.client.get("/books/new/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/books/new/",
            status_code=302,
            target_status_code=200,
        )

    def test_new_book(self):
        factory = RequestFactory()
        request = factory.get("/books/new/")
        request.user = AnonymousUser()
        response = new_book(request)
        self.assertEqual(response.status_code, 200)
        assert "Add a New Book" in str(response.content)


class NewAuthorTests(TestCase):
    def test_authenticated_access(self):
        """
        User needs to login, in order to add a new book
        """
        response = self.client.get("/authors/new/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/authors/new/",
            status_code=302,
            target_status_code=200,
        )

    def test_new_author(self):
        factory = RequestFactory()
        request = factory.get("/authors/new/")
        request.user = AnonymousUser()
        response = new_author(request)
        self.assertEqual(response.status_code, 200)
        assert "Add a New Author" in str(response.content)
