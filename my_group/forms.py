from django import forms
from my_group.models import GroupMember, GroupAdministrator


# for commented context in admin.py file

class GroupMemberChangeListForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=GroupMember.objects.all(), required=False)


class GroupAdministratorChangeListForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=GroupAdministrator.objects.all(), required=False)
