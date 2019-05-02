from django import forms
from django.contrib.auth.models import User
from .models import CommonUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_verification = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=64)
    email_verification = forms.EmailField(max_length=64)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    field_order = ('first_name', 'last_name', 'email', 'email_verification',
                    'password', 'password_verification')

    def clean(self, *args, **kwargs):
        if self.password != self.password_verification:
            raise forms.ValidationError('your passwords do not match')
        if self.email != self.email_verification:
            raise forms.ValidationError('email addresses must be the same')
        else:
            try:
                User.objects.get(email=self.email)
            except User.DoesNotExist:
                pass
            else:
                raise form.ValidationError('User with such email exists')


class CommonUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CommonUser
        fields = ('profile', 'about')
    
    field_order = ('profile', 'about')


class UserLogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')
    
    field_order = ('email', 'password')
