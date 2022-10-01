from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    currency = models.PositiveIntegerField(default=0, blank=True, verbose_name='currency')


class Test(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True)
    point = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=400)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text