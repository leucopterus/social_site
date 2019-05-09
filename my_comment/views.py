from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from my_post.models import Post
from common_user.models import CommonUser
from .models import Comment
# Create your views here.


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('comment_text',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_pk'] = self.kwargs['post_pk']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        commented_post = Post.objects.get(pk=self.kwargs['post_pk'])
        self.object.post = commented_post
        self.object.comment_author = self.request.user.common_user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:post_detail_page',
                            kwargs={'pk': self.kwargs['post_pk']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('posts:post_detail_page',
                            kwargs={'pk': self.kwargs['post_pk']})
