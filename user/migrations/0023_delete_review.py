# Generated by Django 4.2.5 on 2023-10-14 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_customer_name_not_null_customer_locality_not_null_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
