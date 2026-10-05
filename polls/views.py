from django.http import HttpResponse


def index(request):
    return HttpResponse("Привет, мир! Вы на странице с результатами голосования.")
