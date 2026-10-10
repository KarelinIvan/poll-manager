import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Модель вопроса для голосования
    Хранит текст вопроса и дату его публикации
    """

    id = models.AutoField(primary_key=True)  # Явное объявление
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    pub_date = models.DateTimeField(verbose_name="Дата публикации")

    def __str__(self):
        """Возвращает текст вопроса для отображения в админке"""
        return self.question_text

    def was_published_recently(self):
        """Проверяет, был ли вопрос опубликован в последние 24 часа"""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Choice(models.Model):
    """
    Варианты ответа на вопрос
    Связан с моделью Question через ForeignKey.
    Хранит текст ответа и количество набранных голосов.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="Вопрос",
    )
    choice_text = models.CharField(max_length=200, verbose_name="Ответ")
    votes = models.IntegerField(
        default=0, verbose_name="Голоса", help_text="Количество голосов"
    )

    def __str__(self):
        """Возвращает текст ответа"""
        return self.choice_text

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"
