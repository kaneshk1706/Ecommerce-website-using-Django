# Generated by Django 4.2.5 on 2023-10-14 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
    ]
