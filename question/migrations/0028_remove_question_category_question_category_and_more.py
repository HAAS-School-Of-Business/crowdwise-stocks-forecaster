# Generated by Django 4.0.3 on 2022-04-15 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0027_remove_question_category_question_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='question.category'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='voters',
        ),
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(blank=True, null=True, related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
