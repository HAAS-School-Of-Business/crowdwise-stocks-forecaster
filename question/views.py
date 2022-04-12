from pstats import Stats
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# from django.utils.http import is_safe_url

from crowdwise.settings import ALLOWED_HOSTS

from .models import Question
from .forms import ChoiceForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS




def home_view(request, *args, **kwargs):
    all_questions = Question.newmanager.all()
    return render(request, 'question/index.html', {'questions': all_questions}, status=200)

@ login_required
def vote_submit_view(request, *args, **kwargs):
    form = ChoiceForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse({}, status=201)
        if next_url != None :
            return redirect(next_url)
        form=ChoiceForm()
    return render(request, 'question/single.html', context={"form": form}, status=200)


def question_list_view(request, *args, **kwargs):
    """
    REST API
    Return JSON for React, etc.
    """
    qs = Question.objects.all()
    questions_list = [{"id": x.id, "question":x.question, "endDate":x.dateEnd} for x in qs]
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




def vote_single(request, question):

    question = get_object_or_404(Question, slug=question)

    choice_form = ChoiceForm(request.POST)
    if choice_form.is_valid():
        user_choice = choice_form.save(commit=False)
        user_choice.response = question
        user_choice.save()
        return HttpResponseRedirect('/' + question.slug)
    return render(request, 'question/single.html', {'question': question, 'choice_form': choice_form})

