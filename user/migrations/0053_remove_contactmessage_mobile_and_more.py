# Generated by Django 4.2.5 on 2024-04-11 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0052_contactmessage_mobile_contactmessage_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='username',
        ),
    ]
