# Generated by Django 3.0.8 on 2020-08-12 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0003_auto_20200812_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='room_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]