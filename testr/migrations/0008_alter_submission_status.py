# Generated by Django 4.0.3 on 2022-10-16 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testr', '0007_submission_report_json_alter_submission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.TextField(choices=[('WE', 'Waiting Evaluation'), (
                'FL', 'Fail'), ('SC', 'Success')], default='WE', max_length=2),
        ),
    ]
