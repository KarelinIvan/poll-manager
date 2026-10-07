import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    pub_date = models.DateTimeField(verbose_name="Дата публикации")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name="Ответ")
    votes = models.IntegerField(default=0, verbose_name="Голоса")

    def __str__(self):
        return self.choice_text
