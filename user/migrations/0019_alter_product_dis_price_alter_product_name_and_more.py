# Generated by Django 4.2.5 on 2023-10-14 12:52

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_product_dis_price_alter_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dis_price',
            field=models.IntegerField(validators=[user.models.validate_number]),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(validators=[user.models.validate_number]),
        ),
    ]
