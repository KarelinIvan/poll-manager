from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from polls.models import Choice, Question


def index(request):
    """
    Отображает последние пять опубликованных вопросов.
    Получает список объектов Question, отсортированных по дате публикации
    (от новых к старым), и передает их в шаблон для отображения на главной
    странице раздела опросов.
    Args:
        request: Объект HttpRequest, представляющий входящий HTTP-запрос.
    Returns: Объект HttpResponse с отрендеренным HTML-кодом
    страницы polls/index.html.
    """

    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """
    Отображает страницу с деталями конкретного вопроса для голосования.
    Пытается найти вопрос по его первичному ключу (id).
    Если вопрос не найден, автоматически выбрасывает исключение Http404.
    Args:
        request: Объект HttpRequest.
        question_id: Первичный ключ (ID) вопроса, который нужно отобразить.
    Returns: Объект HttpResponse с отрендеренным HTML-кодом
    страницы polls/detail.html.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    """
    Отображает страницу с результатами голосования по конкретному вопросу.
    Аналогично функции detail, получает объект Question по ID и передает его
    в соответствующий шаблон для отображения статистики голосов.
    Args:
        request: Объект HttpRequest.
        question_id: Первичный ключ (ID) вопроса, результаты которого нужно
                    показать.
    Returns: Объект HttpResponse с отрендеренным HTML-кодом
    страницы polls/results.html.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


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
