from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import (View, TemplateView, DetailView,
                                  ListView, UpdateView, DeleteView)
from .models import CommonUser
from .forms import (UserLogInForm, UserRegistrationForm,
                    CommonUserRegistrationForm)
# Create your views here.


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
        common_user = CommonUser.objects.get(user=user)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('for_users:user_home_page', kwargs={'pk': common_user.pk}))
        else:
            return HttpResponseRedirect(reverse('for_users:login_page'))

    form = UserLogInForm()
    context = {
        'form': form
    }
    return render(request, 'login_page.html', context)


def page_for_registeration(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('for_users:welcome'))

    registered = False
    user_form = UserRegistrationForm(request.POST or None)
    user_common_form = CommonUserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid and user_common_form.is_valid:
            user = user_form.save()
            # hash password and save it on db
            user.set_password(user.password)
            user.save()

            user_common = user_common_form.save(commit=False)
            user_common.user = user

            if 'profile' in request.FILES:
                user_common.profile = request.FILES['profile']

            user_common.save()
            registered = True

        else:
            print(user_form.errors, user_common_form.errors)

    context = {
        'form_default_user': user_form,
        'form_common_user': user_common_form,
        'register': registered,
    }
    return render(request, 'registration_page.html', context)


class CommonUserDetailView(DetailView):
    context_object_name = 'common_user_detail'
    model = CommonUser
    template_name = 'for_users/user_info.html'


class CommonUserUpdateView(UpdateView):
    fields = ('user.last_name', 'user.first_name', 'user.email', 'user.password',
              'profile', 'about')
    model = CommonUser


class CommonUserDeleteView(DeleteView):
    model = CommonUser
    success_url = reverse_lazy('for_users:welcome')
