from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Group, GroupMember, GroupAdministrator
from .forms import (GroupMemberChangeListForm,
                    GroupAdministratorChangeListForm)
# Register your models here.


class GroupMemberInLine(admin.TabularInline):
    model = GroupMember
    extra = 1


class GroupGroupAdministratorInLine(admin.TabularInline):
    model = GroupAdministrator
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = (GroupMemberInLine,
               GroupGroupAdministratorInLine)


admin.site.register(Group, GroupAdmin)

# does not work:
# class GroupMemberInline(admin.TabularInline):
#     model = GroupMember

# admin.site.register(Group)


# will cause a change view on admin page group preview
# class GroupMemberChangeList(ChangeList):
#     def __init__(self, *args, **kwargs):
#         super(GroupMemberChangeList, self).__init__(*args, **kwargs)
#         self.list_display = ['action_checkbox',
#                              'name',
#                              'description',
#                              'creator',
#                              'members',
#                              'logo',
#                              'create_data']
#         self.list_display_links = ['name']
#         self.list_editable = ['members']


# class GroupAdmin(admin.ModelAdmin):
#     def get_changelist(self, request, **kwargs):
#         return GroupMemberChangeList

#     def get_changelist_form(self, request, **kwargs):
#         return GroupMemberChangeListForm

# admin.site.register(Group, GroupAdmin)
