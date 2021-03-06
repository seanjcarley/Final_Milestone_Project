# Generated by Django 3.0.8 on 2020-08-25 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0020_auto_20200823_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='ImageComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=256)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.Image')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
