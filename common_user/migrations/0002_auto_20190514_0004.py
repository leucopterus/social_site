# Generated by Django 2.2.1 on 2019-05-13 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuser',
            name='friend_request_receive',
            field=models.ManyToManyField(related_name='_commonuser_friend_request_receive_+', to='common_user.CommonUser'),
        ),
        migrations.AddField(
            model_name='commonuser',
            name='friend_request_send',
            field=models.ManyToManyField(related_name='_commonuser_friend_request_send_+', to='common_user.CommonUser'),
        ),
        migrations.AddField(
            model_name='commonuser',
            name='friends',
            field=models.ManyToManyField(related_name='_commonuser_friends_+', to='common_user.CommonUser'),
        ),
    ]
