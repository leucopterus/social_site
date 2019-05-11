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
