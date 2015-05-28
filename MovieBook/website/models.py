from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    overview = models.CharField(max_length=1000)
    rating = models.FloatField()
    length = models.CharField(max_length=100)
    release_date = models.CharField(max_length = 1000)
    status = models.CharField(max_length=50)
    original_title = models.CharField(max_length=200)
    cover = models.CharField(max_length=300)
    trailer = models.CharField(max_length=300)
    user = models.ManyToManyField(User)
    genre_id = models.ManyToManyField(Genre)
    actor_id = models.ManyToManyField(Actor)
