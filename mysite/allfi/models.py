from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    year = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=500)
    urlposter = models.CharField(max_length=100)
    urlbackdrop = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)
    score = models.FloatField()
