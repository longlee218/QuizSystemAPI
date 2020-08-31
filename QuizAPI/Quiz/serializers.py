from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_new = serializers.CharField(required=False)
    username = serializers.CharField()
    email = serializers.EmailField(read_only=True)

    # def validate_email(self):

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['password', 'password_new', 'username', 'email', 'last_name', 'first_name']


class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    country = serializers.CharField(required=False)
    organization_type = serializers.CharField(required=False)
    organization_name = serializers.CharField(required=False)
    position = serializers.CharField(required=False)

    class Meta:
        model = Instructor
        fields = ['country', 'position',
                  'organization_type', 'organization_name', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.user_type = 2
        user.save()
        instructor, created = Instructor.objects.update_or_create(user=user, **validated_data)
        return instructor

    def update(self, instance, validated_data):
        user_new = UserSerializer(validated_data.get('user', instance.instructor))
        user_new.update(instance, validated_data.get('user', instance.instructor))
        instance.instructor.position = validated_data.get('position', instance.instructor.position)
        instance.instructor.organization_name = validated_data.get('organization_name',
                                                                   instance.instructor.organization_name)
        instance.instructor.organization_type = validated_data.get('organization_type',
                                                                   instance.instructor.organization_type)
        instance.instructor.country = validated_data.get('country', instance.instructor.position)
        instance.instructor.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['room_name', 'instructor', 'status']
        read_only_fields = ('status',)

    def create(self, validated_data):
        instructor = validated_data['instructor']
        room = validated_data.pop('room', [])
        room_name = [room_fields['room_name'] for room_fields in room]
        for i in range(len(room_name)):
            if Room.objects.filter(room_name=room_name[i]):
                continue
            else:
                room = Room.objects.create(room_name=room_name[i], instructor=instructor)
                room.save()
        return room


class RoomNewSeria(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['room_name', 'instructor']


class QuizQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionQuiz
        fields = ("id", "question_type", "description", "explain", "image", "choice", "correct_choice", "quiz_id")
        read_only_fields = ["quiz_id", "id"]

    def create(self, validated_data):
        question_quiz = QuestionQuiz.objects.create(**validated_data)
        question_quiz.save()
        return validated_data


class QuizSerializer(serializers.ModelSerializer):
    quiz_question = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_title', 'subject', 'grade', 'create_at', 'update_at', 'room_id', 'quiz_question']
        read_only_fields = ['update_at', 'create_at', 'room_id']

    def create(self, validated_data):
        quiz = Quiz.objects.create(**validated_data)
        quiz_question = validated_data.pop('quiz_question')
        for i in quiz_question:
            QuestionQuiz.objects.create(**i, quiz=quiz)
        quiz.save()
        return quiz

    def update(self, instance, validated_data):
        quiz_questions = validated_data.pop("quiz_question")
        instance.quiz_title = validated_data.get('quiz_title', instance.quiz_title)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.save()
        exist_id = [c.id for c in instance.quiz_question]
        json_return = []
        for quiz_question in quiz_questions:
            if "id" in quiz_question.keys():
                if QuestionQuiz.objects.filter(id=quiz_question['id']).exists():
                    question_quiz_update = QuestionQuiz.objects.filter(id=quiz_question['id'])
                    question_quiz_update.update(**quiz_question)
                    json_return.append(question_quiz_update)
                else:
                    for quiz in instance.quiz_question:
                        if quiz.id not in exist_id:
                            quiz.delete()
            else:
                question_quiz = QuestionQuiz.objects.create(question_type=quiz_question['question_type'],
                                                            description=quiz_question['description'],
                                                            explain=quiz_question['explain'],
                                                            image=quiz_question['image'],
                                                            choice=quiz_question['choice'],
                                                            correct_choice=quiz_question['correct_choice'],
                                                            quiz=instance)
                json_return.append(question_quiz)
        return json_return


