# Generated by Django 2.2.1 on 2019-05-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(),
        ),
    ]
