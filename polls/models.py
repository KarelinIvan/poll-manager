from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    pub_date = models.DateTimeField(verbose_name="Дата публикации")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name="Ответ")
    votes = models.IntegerField(default=0, verbose_name="Голоса")
