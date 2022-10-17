# Generated by Django 4.0.3 on 2022-10-12 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('professor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('language', models.TextField(choices=[
                 ('CC', 'c/c++'), ('PT', 'python')], default='PT', max_length=2)),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.BinaryField()),
                ('file_name', models.CharField(max_length=128)),
                ('status', models.TextField(choices=[('WS', 'waiting submission'), (
                    'WE', 'waiting evaluation'), ('FL', 'fail'), ('SC', 'success')], default='WS', max_length=2)),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='testr.question')),
                ('student', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('course', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='testr.course')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='testr.section'),
        ),
        migrations.CreateModel(
            name='EvaluationScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.BinaryField()),
                ('script_name', models.CharField(max_length=128)),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='testr.question')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationInputOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField()),
                ('output', models.TextField()),
                ('visible', models.BooleanField()),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='testr.question')),
            ],
        ),
    ]
