from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.paginator import (Paginator, PageNotAnInteger,
                                   EmptyPage)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from .models import Group, GroupMember, GroupAdministrator
from .forms import GroupForm
from my_post.models import Post
# Create your views here.


class GroupListView(ListView):
    model = Group
    paginate_by = 10
    ordering = ('-create_data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_of_groups = Group.get_all_groups()
        paginator = Paginator(list_of_groups, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            groups_per_page = paginator.page(page)
        except PageNotAnInteger:
            groups_per_page = paginator.page(1)
        except EmptyPage:
            groups_per_page = paginator.page(paginator.num_pages)
        context['group_list'] = groups_per_page
        return context


class GroupDetailView(DetailView):
    fields = ('name', 'description', 'logo', 'create_data',
              'members', 'administrators', 'creator')
    context_object_name = 'group_details'
    model = Group

    def get(self, request, *args, **kwargs):
        user = request.user.common_user
        self.kwargs['user'] = user
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_in_group'] = Post.get_group_post_list(
                                                self.kwargs.get('pk'))
        try:
            status = self.kwargs['status']
        except KeyError:
            pass
        else:
            group = Group.objects.get(pk=self.kwargs["pk"])
            if status == 'Join':
                GroupMember.objects.create(
                    user=self.kwargs["user"], group=group)
            if status == 'Leave':
                membership = GroupMember.objects.filter(
                    user=self.kwargs["user"], group=group)
                membership.delete()
        finally:
            return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    # fields = ('name', 'description', 'logo')
    form_class = GroupForm
    model = Group

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user.common_user
        user = self.request.user.common_user
        group = self.object
        group.save()
        GroupAdministrator.objects.create(user=user, group=group)
        GroupMember.objects.create(user=user, group=group)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('groups:group_list')


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    login = '/login/'
    # fields = ('name', 'description', 'logo')
    form_class = GroupForm
    model = Group

    def get_success_url(self):
        return reverse('groups:group_detail', kwargs={'pk': self.kwargs['pk']})


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Group

    def get_success_url(self):
        return reverse_lazy('groups:group_list')


@login_required
def members(request, pk, people, user_pk=None, status=None):
    group = get_object_or_404(Group, pk=pk)
    if user_pk:
        if status == 'remove_from_users':
            group.remove_from_members(user_pk)
        elif status == 'add_to_admins':
            group.add_to_admins(user_pk)
        elif status == 'remove_from_admins':
            group.remove_from_admins(user_pk)
    context = {
        'people': people,
        'group_details': group,
    }
    return render(request, 'my_group/people_edit.html', context)
