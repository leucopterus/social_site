from django import forms
from django.contrib.auth.models import User
from .models import CommonUser


class UserRegistrationForm(forms.ModelForm):

    # this method should be assigned first
    # before called
    @staticmethod
    def create_username(*args, **kwargs):
        # method to create unique username, colled only in POST method
        def random_username(*args, **kwargs) -> str:
            from random import randint, shuffle
            l1 = [randint(48, 57) for _ in range(10)]
            l2 = [randint(65, 90) for _ in range(10)]
            l3 = [randint(97, 122) for _ in range(10)]
            l_all = l1 + l2 + l3
            l = list(map(lambda x: chr(x), l_all))
            shuffle(l)
            return ''.join(l)

        # cycle to change initial username
        while True:
            username = random_username()
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                break
        return username

    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=128, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_verification = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=64)
    email_verification = forms.EmailField(max_length=64)
    # use such form: create_username.__get__(object), to make this method
    # collable
    # because staticmethods are not collable
    my_value = create_username.__get__(object)
    username = forms.CharField(max_length=32, disabled=True,
                               initial=my_value,
                               widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    field_order = ('first_name', 'last_name', 'email', 'email_verification',
                   'password', 'password_verification')

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_verification')
        email1 = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email_verification')

        # check password equality and not user with such email in db
        if password1 != password2:
            raise forms.ValidationError('your passwords do not match')
        if email1 != email2:
            raise forms.ValidationError('email addresses must be the same')
        else:
            try:
                User.objects.get(email=email1)
            except User.DoesNotExist:
                pass
            else:
                raise forms.ValidationError('User with such email exists')


class CommonUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CommonUser
        fields = ('profile', 'about')


class UserLogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

    field_order = ('email', 'password')
