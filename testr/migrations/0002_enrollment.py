# Generated by Django 4.0.3 on 2022-10-13 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('course', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='testr.course')),
                ('student', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-enrolled_at'],
            },
        ),
    ]
