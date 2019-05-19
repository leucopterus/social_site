from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
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
    paginate_by = 10

    def get_queryset(self):
        common_user_id = self.request.user.common_user.id
        # queryset = super().get_queryset()
        # to show post only to their owner
        # queryset = queryset.filter(author__id=related_user_id)
        # queryset.filter(author__user__common_user__id=related_user_id)
        list_of_users_id = CommonUser.people_connected_ids(common_user_id)
        author_qs = Post.objects.filter(author__id__in=list_of_users_id)
        to_user_qs = Post.objects.filter(to_user__id=common_user_id)
        list_of_user_groups = CommonUser.groups_connected_ids(
            common_user_id)
        group_qs = Post.objects.filter(group__in=list_of_user_groups)
        queryset = author_qs.union(to_user_qs, group_qs)
        return queryset.order_by('-create_data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_of_posts = self.get_queryset()
        paginator = Paginator(list_of_posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            post_per_page = paginator.page(page)
        except PageNotAnInteger:
            post_per_page = paginator.page(1)
        except EmptyPage:
            post_per_page = paginator.page(paginator.num_pages)
        context['post_list'] = post_per_page
        return context


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
