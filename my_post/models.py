from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from common_user.models import CommonUser
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(CommonUser,
                               to_field='user',
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='author')
    text = models.TextField()
    create_data = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post:post_detail_view', kwargs={'pk': self.pk})
