# Generated by Django 3.0.8 on 2020-07-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_auto_20200723_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image_data',
            name='focal_length',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
