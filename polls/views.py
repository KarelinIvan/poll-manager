from urllib import response

from django.http import HttpResponse


def index(request):
    return HttpResponse("Привет, мир! Вы на странице с результатами голосования.")


def detail(request, question_id):
    return HttpResponse("Ты смотришь на вопрос %s." % question_id)


def results(request, question_id):
    response = "Вы видите результаты вопроса %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Вы голосуете по воросу %s" % question_id)
