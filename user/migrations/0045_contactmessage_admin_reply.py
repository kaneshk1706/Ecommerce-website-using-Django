# Generated by Django 4.2.5 on 2024-03-15 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0044_customer_gender_alter_customer_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='admin_reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]
