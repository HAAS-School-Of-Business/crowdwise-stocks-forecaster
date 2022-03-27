from pstats import Stats
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Question
from .forms import QuestionForm


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


def vote_submit_view(request, *args, **kwargs):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form=QuestionForm()
    return render(request, 'components/form.html', context={"form": form}, status=200)


def question_list_view(request, *args, **kwargs):
    """
    REST API
    Return JSON for React, etc.
    """
    qs = Question.objects.all()
    questions_list = [{"id": x.id, "question":x.question, "yesVotes":x.yesVotes, "noVotes":x.noVotes} for x in qs]
    data={"response": questions_list}
    return JsonResponse(data)

# Create your views here.
def question_detail_view(request, question_id ,*args, **kwargs):
    """
    REST API
    Return JSON for React, etc.
    """
    data = {
        "isUser": False,
        "id": question_id
        # "image": obj.img.url
    }
    status=200
    try:
        obj = Question.objects.get(id=question_id)
        data['question'] = obj.question
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)
