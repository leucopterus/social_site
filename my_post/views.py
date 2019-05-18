from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from common_user.models import CommonUser
from my_group.models import Group
# Create your views here.


class PostListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Post

    def get_queryset(self):
        related_user_id = self.request.user.common_user.id
        queryset = super().get_queryset()
        # to show post only to their owner
        # queryset = queryset.filter(author__id=related_user_id)
        # queryset.filter(author__user__common_user__id=related_user_id)
        return queryset


class PostDetailView(generic.DetailView):
    context_object_name = 'post_details'
    model = Post


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    # fields = ('text',)
    form_class = PostForm
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['group_pk'] = self.kwargs['group_pk']
        except KeyError:
            pass
        try:
            context['user_pk'] = self.kwargs['user_pk']
        except KeyError:
            pass
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        to_group = None
        to_user = None
        try:
            to_group = get_object_or_404(Group,
                                         pk=self.kwargs['group_pk'])
        except KeyError:
            try:
                to_user = get_object_or_404(CommonUser,
                                            pk=self.kwargs['user_pk'])
            except KeyError:
                to_user = self.request.user.common_user
        finally:
            self.object.author = self.request.user.common_user
            self.object.group = to_group
            self.object.to_user = to_user
            self.object.save()
            return super().form_valid(form)

    def get_success_url(self):
        if not self.kwargs.get('group_pk'):
            common_user = self.object.to_user
            return reverse_lazy('for_users:user_home_page',
                                kwargs={'pk': common_user.pk})
        return reverse_lazy('groups:group_detail',
                            kwargs={'pk': self.kwargs.get('group_pk')})


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    fields = ('text',)
    model = Post


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    model = Post

    def get_success_url(self):
        common_user = self.object.author
        return reverse_lazy('for_users:user_home_page',
                            kwargs={'pk': common_user.pk})
