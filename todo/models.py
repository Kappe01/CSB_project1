from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin = models.IntegerField(default=0)
    security_question = models.CharField(max_length=100)
    security_answer = models.CharField(max_length=100)


class Todo(models.Model):
    todo = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
