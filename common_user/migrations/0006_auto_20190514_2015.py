# Generated by Django 2.2.1 on 2019-05-14 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_user', '0005_auto_20190514_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonuser',
            name='followers',
        ),
        migrations.AlterField(
            model_name='friend',
            name='current_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='common_user.CommonUser'),
        ),
    ]
