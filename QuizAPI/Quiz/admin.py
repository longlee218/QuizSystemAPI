from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Instructor)
admin.site.register(Room)
admin.site.register(Quiz)
admin.site.register(Student)
admin.site.register(QuizCopy1)
admin.site.register(QuizCopy2)
admin.site.register(QuestionQuizCopy1)
admin.site.register(QuestionQuizCopy2)
admin.site.register(DetailResult)
admin.site.register(QuestionQuiz)