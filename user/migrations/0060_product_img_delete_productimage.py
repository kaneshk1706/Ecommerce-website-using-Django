# Generated by Django 5.0.4 on 2024-05-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0059_remove_product_img_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(default='', upload_to='productPics'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
