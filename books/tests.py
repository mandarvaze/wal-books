from django.test import TestCase


class BookIndexViewTests(TestCase):
    def test_authenticated_access(self):
        """
        User needs to login, in order to view the list of books
        """
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 302)
        assert "login" in response.url
