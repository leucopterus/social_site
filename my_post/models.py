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
        return reverse('posts:post_detail_page', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('posts:post_update_page', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('posts:post_delete_page', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.text[:20]}... {self.author}'

    class Meta:
        ordering = ['-create_data']
