# Generated by Django 2.2.1 on 2019-05-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_user', '0003_auto_20190514_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuser',
            name='followers',
            field=models.ManyToManyField(related_name='followers', to='common_user.Friend'),
        ),
    ]