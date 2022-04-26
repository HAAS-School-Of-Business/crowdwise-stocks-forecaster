from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from question.models import Question
from django.http import JsonResponse
from django.contrib.auth import login

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "404.html", {})
