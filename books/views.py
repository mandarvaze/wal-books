from django.http import HttpResponse


def index(request):
    return HttpResponse("Read books and be better!.")
