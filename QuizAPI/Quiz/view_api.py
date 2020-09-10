from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse, QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from . import token_setting
from django.conf import settings
from . import utils
from .models import *
from .serializers import *


def data_json_return(success, messages, data=None):
    return {'success': success, 'messages': messages, 'data': data}


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def user_info(request):
    try:
        user = request.user
        status_code = status.HTTP_200_OK
        response = {}
        if user.user_type == '2':
            serializer = InstructorSerializer(Instructor.objects.get(user=user))
            response = {
                'success': '1',
                'status': status_code,
                'user': serializer.data
            }
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            'success': '0',
            'status': status_code,
        }
    return Response(response, status=status_code)


@api_view(['GET'])
def get_info_instructor(request):
    instructor = Instructor.objects.all()
    serializer = InstructorSerializer(instructor, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Register new user


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def post_info_instructor(request):
    serializer = InstructorSerializer(data=request.data)
    if serializer.is_valid(raise_exception=ValueError):
        user = serializer.create(validated_data=request.data)
        token = RefreshToken.for_user(user.user).access_token
        current_site = get_current_site(request).domain
        link = reverse('teacher:email-verify')
        absurl = 'http://' + current_site + link + '?token=' + str(token)
        data = {
            'email_body': 'Hi ' + user.user.username + ' .Use link below to verify your email \n' + absurl,
            'email_subject': 'Verify your email',
            'email_to': user.user.email
        }
        status_email = utils.Util.send_email(data=data)
        if status_email:
            return JsonResponse({'instructor': serializer.data, 'token': Token.objects.create(user=user.user).key},
                                status=status.HTTP_201_CREATED)
        Instructor.objects.get(user=user).delete()
        user.token.delete()
        user.delete()
        return JsonResponse({'error': 'Email not valid'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


# login simple handle
@api_view(['POST'])
def login_user(request):
    # print(request.data)
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        if user:
            refresh = token_setting.UserTokenObtainPairSerializer.get_token(user)
            data = {
                'refresh_toke': str(refresh),
                'access_token': str(refresh.access_token),
                'refresh_expire': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                'access_expire': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            }
            login(request, user)
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(data_json_return(0, 'Email or password is not correct'), status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'messages': serializer.error_messages},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        request_data = request.data.copy()
        request_data['username'] = request.user.get_username()
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.update(request.user, request.data)
            return JsonResponse({'messages': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_email_reset_password(request):
    email = request.data['email']
    # user = User.objects.get(email=email)
    user = get_object_or_404(User, email=email)
    token = Token.objects.get(user_id=user.id).key
    current_site = get_current_site(request).domain
    link = reverse('teacher:forgot-password')
    absurl = 'http://' + current_site + link + '?token=' + str(token)
    data = {
        'email_body': 'HI ' + user.username + ' .Use link below to reset your password \n' + absurl,
        'email_subject': 'Reset password',
        'email_to': user.email
    }
    status_email = utils.Util.send_email(data=data)
    return JsonResponse(data_json_return(1, "Success"), status.HTTP_200_OK)


@api_view(['POST'])
def forgot_password(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_info_instructor(request):
    if request.method == 'POST':
        request_data = request.data.copy()
        print(request_data)
        request_data['user']['username'] = request.user.get_username()
        request_data['user']['password'] = request.user.password
        serializer = InstructorSerializer(data=request_data)
        if serializer.is_valid():
            serializer.update(request.user, request_data)
            return JsonResponse({'messages': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        request_data = request.data.copy()
        success = request.user.check_password(request_data['old_password'])
        if success:
            if request_data['new_password'] == request_data['new_password_confirm']:
                request.user.set_password(request_data['new_password_confirm'])
                request.user.save()
                return JsonResponse(data_json_return(1, 'Your password have been change'), status=status.HTTP_200_OK)
            return JsonResponse(data_json_return(0, 'Your password are not merge'), status=status.HTTP_200_OK)
        return JsonResponse(data_json_return(0, 'Wrong password'), status=status.HTTP_200_OK)
    return JsonResponse(data_json_return(0, 'Not allowed this method'), status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object()

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(data_json_return(0, 'Wrong password'), status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(data_json_return(1, 'Success update'), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return JsonResponse({'type': 'success'}, status=status.HTTP_200_OK)


# create multi room and get room
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_show_room(request):
    context = {}
    if request.method == 'POST':
        data = request.data
        data['instructor'] = request.user.instructor
        serializer = RoomSerializer(data=data)
        room_name = [room_fields['room_name'] for room_fields in data['room']]
        for i in range(len(room_name)):
            if Room.objects.filter(room_name=room_name[i]).exists():
                context['error'] = 'Room have exists'
                return JsonResponse(context, status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.create(validated_data=data)
            context['room'] = serializer.data
            context['messages'] = 'Success'
            return Response(context, status.HTTP_200_OK)
    if request.method == 'GET':
        pk = request.GET.get('pk', None)
        if pk is None:
            room = Room.objects.filter(instructor=request.user.instructor)
            serializer = RoomSerializer(room, many=True)
            context['room'] = serializer.data
            context['messages'] = 'Success'
            return Response(context, status.HTTP_200_OK)
        try:
            room = Room.objects.filter(id=pk)
            serializer = RoomSerializer(room, many=True)
            context['room'] = serializer.data
            context['messages'] = 'Success'
            return Response(context, status.HTTP_200_OK)
        except Room.DoesNotExist:
            context['error'] = 'Error'
            return Response(context, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def room_action(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        if Student.objects.get(room_id=pk) is None:
            data = JSONParser().parse(request)
            serializer = RoomSerializer(room, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"messages": "Can't not update"}, status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == 'DELETE':
        quiz = Quiz.objects.filter(room_id=pk)
        quiz.delete()
        room.delete()
        return JsonResponse({}, status=204)


class RoomListPaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page'
    max_page_size = 20


# room_search
class RoomListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ('room_name', 'status', 'instructor__user__username')
    filterset_fields = ('room_name', 'status', 'instructor__user__username')
    ordering_fields = ('room_name', 'id', 'create_at')
    pagination_class = RoomListPaginator


# create QUIZ
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def quiz_action(request, pk=None):
    context = {}
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        context['quiz'] = serializer.data
        return JsonResponse(context, status=status.HTTP_200_OK)
    if request.method == 'POST' or request.method == 'PUT':
        serializer = QuizSerializer(data=request.data['quiz'])
        if serializer.is_valid():
            data_return = serializer.update(quiz, request.data['quiz'])
            context['messages'] = 'Update success'
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def render_question(request, pk=None):
    context = {}
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz_copy1 = QuizCopy1.objects.create(quiz_id=quiz.id, quiz_title=quiz.quiz_title, subject=quiz.subject,
                                              grade=quiz.grade, room=quiz.room_id)
        list_question = quiz.questionquiz_set.all()
        for i in list_question:
            QuestionQuizCopy1.objects.create(question_type=i.question_type, description=i.description,
                                             explain=i.explain,
                                             image=i.image, choice=i.choice, correct_choice=i.correct_choice,
                                             quiz_copy_1=quiz_copy1)
        serializer = QuizSerializer(quiz)
        return Response(data_json_return(1, "Success render", serializer.data), status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_quiz(request):
    if request.method == 'GET':
        quiz = Quiz.objects.filter(room__instructor__user=request.user)
        if "q" in request.GET:
            quiz = quiz.filter(quiz_title__contains=request.GET['q'])
        serializer = QuizSerializer(quiz, many=True)
        if quiz.exists() is False:
            return Response(data_json_return(1, "Don't have", serializer.data), status.HTTP_200_OK)
        return Response(data_json_return(1, "Success", serializer.data), status=status.HTTP_200_OK)


class QuizListPaginator(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'
    max_page_size = 20


class QuizListView(generics.ListAPIView):
    permission_classes([IsAuthenticated])
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ('quiz_title', 'subject', 'create_at', 'room__id', 'questionquiz__description')
    filterset_fields = ('quiz_title', 'subject', 'create_at', 'room__id', 'questionquiz__description')
    ordering_fields = ('quiz_title', 'id', 'create_at')
    pagination_class = QuizListPaginator



# @api_view(['POST', 'GET'])
# @permission_classes(IsAuthenticated)
# def launch_quiz(request):
#     pass
# =============================================================


class RoomList(ListCreateAPIView):
    serializer_class = RoomNewSeria
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        for i in range(len(self.request.data)):
            serializer.save(instructor=self.request.user.instructor)

    def get_queryset(self):
        return Room.objects.filter(instructor=self.request.user.instructor)


class RoomListDetailView(RetrieveDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Room.objects.filter(instructor=self.request.user.instructor)
