# Generated by Django 3.0.8 on 2020-08-31 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20200811_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='comment',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
