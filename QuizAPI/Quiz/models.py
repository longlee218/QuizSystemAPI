from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

# Create your models here.

user_type_date = (
    ('1', 'Admin'),
    ('2', 'Teacher'),
    ('3', 'Student'),
)

organization_type_data = (
    ('1', 'Primary/Secondary School'),
    ('2', 'University'),
    ('3', 'Corporate'),
    ('4', 'Other'),
)

status_date = (
    ('1', 'Activate'),
    ('2', 'Block'),
    ('3', 'Maintenance')
)

grade_data = (
    ('1', 'Primary/Secondary School'),
    ('2', 'University'),
    ('3', 'Advance'),
    ('4', 'Other')
)
question_type_data = (
    ('1', 'MultipleChoice'),
    ('2', 'TrueFalse'),
    ('3', 'ShortAnswer'),
)


class User(AbstractUser):
    user_type = models.CharField(choices=user_type_date, max_length=1, default=1, null=False, blank=True)


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    organization_type = models.CharField(choices=organization_type_data, max_length=4, null=False)
    organization_name = models.CharField(max_length=125, null=False)
    position = models.CharField(max_length=125, null=True, blank=True)


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=status_date, default=1, null=False)
    room_name = models.CharField(max_length=255, default="Room Default")


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=255, default='Quiz title', blank=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=1, default=4, blank=True, choices=grade_data)
    choose = models.IntegerField(default=0, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    @property
    def quiz_question(self):
        return self.questionquiz_set.all()


class QuizCopy1(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_title = models.CharField(max_length=255, default='Quiz title', blank=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=1, default=4, blank=True, choices=grade_data)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    room = models.IntegerField(default=1)
    quiz_id = models.IntegerField(null=False, default=100)


class QuizCopy2(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_title = models.CharField(max_length=255, default='Quiz title', blank=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=1, default=4, blank=True, choices=grade_data)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    room = models.IntegerField(default=1)


class QuestionQuiz(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.TextField(max_length=1, choices=question_type_data)
    description = models.CharField(max_length=255, null=False, blank=False)
    explain = models.TextField(null=True)
    image = models.FileField(null=True)
    choice = models.TextField()
    correct_choice = models.TextField()


class QuestionQuizCopy1(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_copy_1 = models.ForeignKey(QuizCopy1, on_delete=models.CASCADE)
    question_type = models.TextField(max_length=1, choices=question_type_data)
    description = models.CharField(max_length=255, null=False, blank=False)
    explain = models.TextField(null=True)
    image = models.FileField(null=True)
    choice = models.TextField()
    correct_choice = models.TextField()


class QuestionQuizCopy2(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_copy_2 = models.ForeignKey(QuizCopy2, on_delete=models.CASCADE)
    question_type = models.TextField(max_length=1, choices=question_type_data)
    description = models.CharField(max_length=255, null=False, blank=False)
    explain = models.TextField(null=True)
    image = models.FileField(null=True)
    choice = models.TextField()
    correct_choice = models.TextField()


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=125, null=False, blank=False)
    room_id = models.IntegerField(blank=True, null=True)


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    quiz_copy_2 = models.ForeignKey(QuizCopy2, on_delete=models.CASCADE)
    score = models.CharField(max_length=10)
    percent = models.CharField(max_length=10)
    finish_at = models.DateTimeField()


class DetailResult(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    choice_answer = models.TextField()
    correct_choice = models.TextField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            pass
        elif instance.user_type == 2:
            Instructor.objects.create(user=instance)
        elif instance.user_type == 3:
            pass


# @receiver(post_save, sender=Quiz)
# def create_quiz_or_update(sender, instance, created, **kwargs):
#     if created:
#         quiz1 = QuizCopy1.objects.create(quiz_title=instance.quiz_title, subject=instance.subject,
#                                          grade=instance.grade, create_at=instance.create_at,
#                                          update_at=instance.update_at, room=instance.room_id)
#         quiz1.save()

