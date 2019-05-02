from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import (UserLogInForm, UserRegistrationForm,
                    CommonUserRegistrationForm)
# Create your views here.


@login_required
def welcome_page(request):
    context = {}
    return render(request, 'welcome_page.html', context)


@login_required
def page_for_log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('for_users:login_page'))


def page_for_log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('for_users:welcome'))
        else:
            return HttpResponseRedirect(reverse('for_users:login_page'))
    form = UserLogInForm()
    context = {
        'form': form
    }
    return render(request, 'login_page.html', context)


def page_for_registeration(request):
    context = {}
    return render(request, 'registration_page.html', context)
