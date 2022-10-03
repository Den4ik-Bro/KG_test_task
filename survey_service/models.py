from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    currency = models.PositiveIntegerField(default=0, blank=True, verbose_name='currency')
    passed_surveys = models.ManyToManyField('Survey', blank=True, verbose_name='passed survey')
    color = models.CharField(max_length=50, default='green', blank=True, verbose_name='color')
    # user_colors для того, что бы уже купленный цвет сохранялся у пользователя
    # и можно было бы сделать метод update и там их менять
    user_colors = models.ManyToManyField('Color', blank=True, verbose_name='user color list')


class Color(models.Model):
    COLOR_CHOICES = [
        ('Pink', 'pink'),
        ('Blue', 'blue'),
        ('White', 'white'),
        ('Yellow', 'yellow'),
        ('Black', 'black'),
    ]
    color = models.CharField(choices=COLOR_CHOICES, max_length=25, verbose_name='color')
    price = models.PositiveIntegerField(verbose_name='price')

    def __str__(self):
        return self.color


class Survey(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True)
    point = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Survey'


class Question(models.Model):
    text = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
