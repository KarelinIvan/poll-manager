from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question


class IndexView(generic.ListView):
    """
    Получает список объектов Question, отсортированных по дате публикации
    (от новых к старым), и передает их в шаблон для отображения на главной
    странице раздела опросов.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Отображает последние пять опубликованных вопросов."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DeleteView):
    """
    Отображает страницу с деталями конкретного вопроса для голосования.
    Пытается найти вопрос по его первичному ключу (id).
    """

    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """
    Отображает страницу с результатами голосования по конкретному вопросу.
    Аналогично функции detail, получает объект Question по ID и передает его
    в соответствующий шаблон для отображения статистики голосов.
    """

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Обрабатывает отправку формы голосования (POST-запрос).
    Пытается найти выбранный пользователем вариант ответа (Choice) и увеличить
    счетчик голосов с помощью F-объекта для предотвращения гонок условий.
    При успехе перенаправляет на страницу результатов.
    Если выбор не сделан или вариант не найден, повторно отображает форму
    с сообщением об ошибке.
    Args:
        request: Объект HttpRequest. Ожидается метод POST с данными формы.
        question_id: Первичный ключ (ID) вопроса, за который голосуют.
    Returns: HttpResponseRedirect на страницу результатов при успехе.
    HttpResponse с формой detail.html и сообщением об ошибке при неудаче.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # KeyError: в POST-данных не было ключа 'choice'.
        # Choice.DoesNotExist: ID варианта не привязан к этому вопросу.
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "Вы не выбрали вариант."},
        )
    else:
        # F-объект выполняет инкремент на стороне БД (votes = votes + 1)
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
