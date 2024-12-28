# Generated by Django 5.0.4 on 2024-05-10 05:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0055_contactmessage_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_username',
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='user.product'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='user.product')),
            ],
        ),
    ]
