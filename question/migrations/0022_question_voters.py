# Generated by Django 4.0.3 on 2022-04-15 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0021_alter_choice_options_remove_choice_answered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
