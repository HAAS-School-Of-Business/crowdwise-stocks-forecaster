# Generated by Django 4.0.3 on 2022-04-14 09:08

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='correct_answers',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='questions_answered',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default=None, upload_to=accounts.models.user_directory_path),
        ),
    ]
