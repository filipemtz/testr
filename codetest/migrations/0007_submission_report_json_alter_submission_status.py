# Generated by Django 4.0.3 on 2022-10-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codetest', '0006_question_time_limit_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='report_json',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.TextField(choices=[('WE', 'Waiting Evaluation'), ('RC', 'Received by AutoJudge'), ('FL', 'Fail'), ('SC', 'Success')], default='WE', max_length=2),
        ),
    ]
