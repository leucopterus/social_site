from django.db import models
from django.utils import timezone
from django.urls import reverse
from common_user.models import CommonUser
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, default='')
    creator = models.ForeignKey(CommonUser,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='creator')
    admins = models.ManyToManyField(CommonUser,
                                    through='GroupAdministrator',
                                    related_name='admins')
    members = models.ManyToManyField(CommonUser,
                                     through='GroupMember',
                                     related_name='members')
    logo = models.ImageField(upload_to='group_profile',
                             default='group_profile/group_default.png',
                             blank=True,
                             verbose_name='group_logo')
    create_data = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-create_data']

    @classmethod
    def get_all_groups(cls):
        return cls.objects.all()

    def get_absolute_url(self):
        return reverse('groups:group_list')

    def get_detail_url(self):
        return reverse('groups:group_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('groups:delete_group', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('groups:update_group', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(CommonUser, related_name='user_groups',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is a member of group {self.group}'

    class Meta:
        unique_together = ['group', 'user']


class GroupAdministrator(models.Model):
    group = models.ForeignKey(Group,
                              related_name='administrators',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(CommonUser,
                             related_name='administrator_user_groups',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is an admin of group {self.group}'

    class Meta:
        unique_together = ['group', 'user']
