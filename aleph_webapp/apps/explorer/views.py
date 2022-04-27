from django.http import HttpResponse
from django.shortcuts import render


def Explorer(request):
    return render(request, "explorer/explorer.html")

