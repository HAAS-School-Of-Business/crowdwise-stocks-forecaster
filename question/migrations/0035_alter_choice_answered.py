# Generated by Django 4.0.3 on 2022-04-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0034_choice_answered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='answered',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, null=True),
        ),
    ]
