# Generated by Django 4.2.5 on 2024-03-14 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0043_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(default='Other', max_length=15),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.CharField(max_length=15),
        ),
        migrations.AddConstraint(
            model_name='customer',
            constraint=models.CheckConstraint(check=models.Q(('gender__isnull', False)), name='gender_not_null'),
        ),
    ]
