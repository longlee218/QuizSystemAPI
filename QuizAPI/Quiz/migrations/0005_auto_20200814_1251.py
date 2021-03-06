# Generated by Django 3.0.8 on 2020-08-14 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0004_student_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='choose',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='QuestionQuiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_type', models.TextField(choices=[('1', 'MultipleChoice'), ('2', 'TrueFalse'), ('3', 'ShortAnswer')], max_length=1)),
                ('description', models.CharField(max_length=255)),
                ('explain', models.TextField(null=True)),
                ('image', models.FileField(null=True, upload_to='')),
                ('choice', models.TextField()),
                ('correct_choice', models.TextField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.QuizCopy1')),
            ],
        ),
    ]
