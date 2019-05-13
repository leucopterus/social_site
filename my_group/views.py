from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from .models import Group, GroupMember, GroupAdministrator
# Create your views here.


class GroupListView(ListView):
    model = Group


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
        try:
            status = self.kwargs['status']
        except KeyError:
            pass
        else:
            # print('-'*100)
            # print(f'status: {status}')
            # print('-'*100)
            # print(f'group pk: {self.kwargs["pk"]}')
            # print('-'*100)
            # print(f'user: {self.kwargs["user"]}')
            # print('-'*100)
            group = Group.objects.get(pk=self.kwargs["pk"])
            # print(f'group: {group}')
            # print('-'*100)
            # print(f'people in group: {group.members.count()}')
            if status == 'Join':
                GroupMember.objects.create(
                    user=self.kwargs["user"], group=group)
            if status == 'Leave':
                membership = GroupMember.objects.filter(
                    user=self.kwargs["user"], group=group)
                membership.delete()
            # print('-'*100)
            # print(f'people in group: {group.members.count()}')
            # print('-'*100)
        finally:
            return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    fields = ('name', 'description', 'logo')
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
    fields = ('name', 'description', 'logo')
    model = Group

    def get_success_url(self):
        return reverse('groups:group_detail', kwargs={'pk': self.pk})


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Group

    def get_success_url(self):
        return reverse_lazy('groups:group_list')
