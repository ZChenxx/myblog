from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import Article


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
