# Generated by Django 3.0.8 on 2020-08-12 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0002_auto_20200811_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizcopy1',
            name='room',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='quizcopy2',
            name='room',
            field=models.IntegerField(default=1),
        ),
    ]
