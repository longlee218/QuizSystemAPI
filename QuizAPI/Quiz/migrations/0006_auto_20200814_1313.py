# Generated by Django 3.0.8 on 2020-08-14 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0005_auto_20200814_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.Quiz'),
        ),
    ]