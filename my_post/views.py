from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
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
    fields = ('text',)
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_id'] = self.kwargs['group_id']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user.common_user
        self.object.posts_in_group = self.request.group_id
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        common_user = self.object.author
        return reverse_lazy('for_users:user_home_page',
                            kwargs={'pk': common_user.pk})


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
