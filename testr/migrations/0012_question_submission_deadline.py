# Generated by Django 4.0.3 on 2023-04-05 14:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testr', '0011_questionfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='submission_deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]