# Generated by Django 4.2.5 on 2023-09-23 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Cam', 'Camera'), ('Dig', 'DigitalCamera'), ('Hea', 'Headphone'), ('Lap', 'Laptop'), ('Sma', 'Smartwatches'), ('Tel', 'Television'), ('Mob', 'Mobiles'), ('Fas', 'Fashion'), ('Fur', 'Furniture'), ('Gro', 'Grocery'), ('App', 'Appliances'), ('Toy', 'Toys'), ('Spo', 'Sports')], default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='productPics'),
        ),
    ]
