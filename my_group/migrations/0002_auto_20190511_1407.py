# Generated by Django 2.2.1 on 2019-05-11 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='common_user.CommonUser'),
        ),
    ]