from django import forms
from mediumeditor.widgets import MediumEditorTextarea
from my_group.models import GroupMember, GroupAdministrator, Group


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'description', 'logo')

        widgets = {
            'description': MediumEditorTextarea(),
        }


# for commented context in admin.py file

class GroupMemberChangeListForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=GroupMember.objects.all(), required=False)


class GroupAdministratorChangeListForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=GroupAdministrator.objects.all(), required=False)
