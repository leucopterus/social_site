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
    friends = models.ManyToManyField('self', related_name='friends')
    friend_request_sent = models.ManyToManyField('self',
                                                 related_name='sent',
                                                 symmetrical=False)
    friend_request_received = models.ManyToManyField('self',
                                                     related_name='received',
                                                     symmetrical=False)

    @classmethod
    def add_friend(cls, sent_id, received_id):
        if sent_id != received_id:
            sent = cls.objects.get(pk=sent_id)
            received = cls.objects.get(pk=received_id)
            if received not in sent.friend_request_received.all():
                sent.friend_request_sent.add(received)
                received.friend_request_received.add(sent)
            else:
                sent.friend_request_received.remove(received)
                received.friend_request_sent.remove(sent)
                sent.friends.add(received)

    @classmethod
    def remove_friend(cls, sent_id, received_id):
        if sent_id != received_id:
            sent = cls.objects.get(pk=sent_id)
            received = cls.objects.get(pk=received_id)
            if received in sent.friends.all():
                sent.friends.remove(received)
                sent.friend_request_received.add(received)
                received.friend_request_sent.add(sent)
            elif received in sent.friend_request_sent.all():
                sent.friend_request_sent.remove(received)
                received.friend_request_received.remove(sent)

    @classmethod
    def get_friends_list(cls, commonuser_id):
        return cls.objects.get(pk=commonuser_id).friends.all().order_by('?')

    @classmethod
    def get_friend_sent_list(cls, commonuser_id):
        return cls.objects.get(pk=commonuser_id).friend_request_sent.all().order_by('?')

    @classmethod
    def get_friend_received_list(cls, commonuser_id):
        return cls.objects.get(pk=commonuser_id).friend_request_received.all().order_by('?')

    @classmethod
    def people_connected_ids(cls, user_id) -> list:
        ''' this method returns user, his friends,
        and sent request to friends ids in list output '''
        list_of_ids = []
        list_of_ids.append(user_id)
        user = cls.objects.get(id=user_id)
        friends_qs = user.friends.all()
        friend_request_sent_qs = user.friend_request_sent.all()
        for friend in friends_qs:
            list_of_ids.append(friend.id)
        for friend in friend_request_sent_qs:
            list_of_ids.append(friend.id)
        return list_of_ids

    @classmethod
    def groups_connected_ids(cls, user_id) -> list:
        ''' this method returns list of user groups' id '''
        list_of_groups = []
        user = cls.objects.get(id=user_id)
        groups_qs = user.user_groups.all()
        for group in groups_qs:
            list_of_groups.append(group.group)
        return list_of_groups

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('for_users:user_home_page', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
