from django.db import models

class Movie(models.Model):
    movie_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    like_count = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
