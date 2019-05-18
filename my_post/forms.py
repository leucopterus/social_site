from django import forms
from mediumeditor.widgets import MediumEditorTextarea
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', )

        widgets = {
            'text': MediumEditorTextarea(),
        }
