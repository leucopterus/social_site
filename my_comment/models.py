from django.db import models
from django.utils import timezone
from django.urls import reverse
from common_user.models import CommonUser
from my_post.models import Post
# Create your models here.


class Comment(models.Model):
    comment_author = models.ForeignKey(CommonUser, to_field='user',
                                       null=True,
                                       on_delete=models.SET_NULL,
                                       related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments_to_post')
    # related_name is defined to refer from Post model to Comment by colling:
    # post_details.comments_to_post.all in post_detail.html to show
    # all comments under the post
    comment_text = models.TextField()
    create_data = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('posts:post_detail_page', kwargs={'pk': self.post.pk})

    def get_create_url(self):
        return reverse('comments:comment_create',
                       kwargs={'post_pk': self.post.pk})

    def get_delete_url(self):
        return reverse('comments:comment_delete',
                       kwargs={'post_pk': self.post.pk,
                               'pk': self.pk})

    def __str__(self):
        return f'{self.comment_text[:10]}'

    class Meta:
        ordering = ['create_data']
