from pstats import Stats
from secrets import choice
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# from django.utils.http import is_safe_url

from crowdwise.settings import ALLOWED_HOSTS

from .models import Question, join_q, Choice
from .forms import ChoiceForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS




def home_view(request, *args, **kwargs):
    all_questions = Question.newmanager.all()
    if not request.user.is_anonymous:
        if request.method == "GET":
            profile = request.user.profile
            user = request.user
            choices = user.profile.choices.all()
            return render(request, 'question/index.html', {'questions': all_questions, 'user':user, 'profile':profile, 'choices': choices}, status=200)
    else:
        return render(request, 'question/index.html', {'questions': all_questions, 'user':None, 'profile':None}, status=200)

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

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_updates(request, question):
    q = Question.objects.get(slug=question)



@ login_required
def vote_single(request, question):
    voted = False
    response = None
    q = Question.objects.get(slug=question)
    superuser = request.user.is_superuser
    if request.method == "POST" :
        form = ChoiceForm()
        if request.POST.get('Yes') and not voted:
            response=True
            q.addYesVote()
        elif request.POST.get('No') and not voted:
            response=False
            q.addNoVote()
        join_q(request, question, response)
        obj = form.save(commit=False)
        obj.question = q
        obj.user = request.user
        obj.answered = True
        obj.response =response
        obj.save()
        request.user.profile.choices.add(obj)
        return HttpResponseRedirect('/' + q.slug +'/?voted=True' )
    else:
        form = ChoiceForm()
        if 'voted' in request.GET:
            voted = True
        if request.method == "GET" and q in request.user.profile.questions_answered.all():
            response = Choice.objects.get(user=request.user, question=q).response
            print(response)
    return render(request, 'question/single.html', {'question': q, 'form':form, 'superuser': superuser,'voted': voted, 'user': request.user, 'response': response})

