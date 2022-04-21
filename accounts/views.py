from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm, UserProfileForm
from .tokens import account_activation_token
from .models import Profile
from question.models import Question
from django.http import JsonResponse



@ login_required
def vote(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        q = get_object_or_404(Question, id=id)
        if q.likes.filter(id=request.user.id).exists():
            q.likes.remove(request.user)
            q.like_count -= 1
            result = q.like_count
            q.save()
        else:
            q.likes.add(request.user)
            q.like_count += 1
            result = q.like_count
            q.save()

        return JsonResponse({'result': result, })


@ login_required
def favourite_list(request):
    new = Question.newmanager.filter(favourites=request.user)
    return render(request,
                  'accounts/favourites.html',
                  {'new': new})


@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Question, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpsResponseRedirect(request.META['HTTP_REFERER'])


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
    else:
        return {
            'NotLoggedIn': User.objects.none()
        }


@login_required
def profile(request):
    all_questions = Question.newmanager.all()

    return render(request,
                  'accounts/profile.html',
                  {'questions': all_questions}, status=200)


@login_required
def edit(request):
    if request.method == 'POST':

        user_form = UserEditForm(instance=request.user ,data=request.POST)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_user(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')





def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
        return render(request, 'accounts/profile.html', {'form': registerForm})
            # current_site = get_current_site(request)
            # subject = 'Activate your Account'
            # message = render_to_string('registration/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject=subject, message=message)
            # return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': registerForm})


# def activate(request, uidb64, token):
#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('login')
#     else:
#         return render(request, 'registration/activation_invalid.html')