from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CommonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(verbose_name='Profile Photo',
                                upload_to='user_profile',
                                default='default_profile.png')
    about = models.CharField(max_length=512, blank=True)
    registration_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
