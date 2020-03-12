from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)
    # TODO: Add user who created this entru. Useful if we need to restrict only the creator to update.

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
