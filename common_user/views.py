from django.shortcuts import (render, redirect, HttpResponseRedirect,
                              get_object_or_404)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (View, TemplateView, DetailView,
                                  ListView, UpdateView, DeleteView)
from django.views.generic.edit import DeletionMixin
from .models import CommonUser
from my_post.models import Post
from .forms import (UserLogInForm, UserRegistrationForm,
                    CommonUserRegistrationForm)
# Create your views here.


def welcome_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('for_users:user_home_page',
                                kwargs={'pk': request.user.common_user.pk}))
    context = {}
    return render(request, 'welcome_page.html', context)


@login_required
def page_for_log_out(request):
    thanks = f'Thank you, {request.user.common_user}, for visiting us! See you next time!'
    logout(request)
    context = {'thanks': thanks}
    return render(request, 'welcome_page.html', context)


def page_for_log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('for_users:login_page'))
        user = authenticate(username=username, password=password)
        try:
            common_user = CommonUser.objects.get(user=user)
        except CommonUser.DoesNotExist:
            return HttpResponseRedirect(reverse('for_users:login_page'))

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('for_users:user_home_page', 
                                        kwargs={'pk': common_user.pk}))
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


class CommonUserDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'common_user_detail'
    model = CommonUser
    template_name = 'for_users/user_info.html'

    def get(self, request, *args, **kwargs):
        visitor = request.user.common_user
        self.kwargs['visitor'] = visitor
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # if in url we send pk, so we can grab it by accessing
        # not request.pk but just only pk
        # but before that we should make pk accesible:
        # context['pk'] = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        common_user_id = self.kwargs['pk']
        context['post_list'] = None
        context['friends'] = None
        context['friends_sent'] = None
        context['friends_received'] = None
        friends_qs = CommonUser.get_friends_list(common_user_id)
        friend_request_sent_qs = CommonUser.get_friend_sent_list(common_user_id)
        friend_request_received_qs = CommonUser.get_friend_received_list(
            common_user_id)
        list_of_posts = Post.get_to_user_post_list(self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        if list_of_posts:
            context['post_list'] = list_of_posts
        if friends_qs:
            context['friends'] = friends_qs
        if friend_request_sent_qs:
            context['friends_sent'] = friend_request_sent_qs
        if friend_request_received_qs:
            context['friends_received'] = friend_request_received_qs
        return context


class CommonUserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('profile', 'about')
    model = CommonUser
    template_name = 'for_users/commonuser_form.html'


class CommonUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CommonUser
    template_name = 'for_users/commonuser_confirm_delete.html'
    # success_url = reverse_lazy('for_users:welcome')

    def delete(self, request, **kwargs):
        user_pk = request.user.pk
        user = User.objects.get(pk=user_pk)
        user.delete()
        return redirect(reverse('for_users:welcome'))


@login_required
def add_or_remove_friend(request, pk, status):
    if request.user.common_user.pk != pk:
        if status == 'add':
            CommonUser.add_friend(request.user.common_user.pk, pk)
        elif status == 'remove':
            CommonUser.remove_friend(request.user.common_user.pk, pk)

    return redirect(reverse_lazy('for_users:user_home_page',
                    kwargs={'pk': pk}))
