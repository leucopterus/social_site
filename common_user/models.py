from django.urls import reverse
from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


class CommonUser(models.Model):
    user = models.OneToOneField('auth.User', unique=True,
                                related_name='common_user',
                                on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='user_profile',
                                default='user_profile/default_profile.png',
                                verbose_name='Profile', blank=True)
    about = models.TextField(max_length=512, blank=True)
    registration_date = models.DateTimeField(auto_now=True)
    # friends = models.ManyToManyField(CommonUser)

    def get_absolute_url(self):
        return reverse('for_users:user_home_page', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
