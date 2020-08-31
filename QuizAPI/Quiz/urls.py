from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from rest_framework_simplejwt.views import TokenRefreshView
from .view_api import *
from . import token_setting
from . import views

app_name = 'teacher'
urlpatterns = [
    url(r'^api-token-refresh$', refresh_jwt_token, name='token-refresh'),
    url(r'^api-token-verify/', token_setting.UserTokenObtainPairView.as_view(), name='token-verify'),
    url(r'^verify$', verify_jwt_token),
    url(r'^api-info/$', user_info, name='info_user'),
    url(r'^api/register/$', post_info_instructor, name='pos_info'),
    url(r'^email-verify$', views.homepage, name='email-verify'),
    url(r'^email/reset/password/$', send_email_reset_password, name='send-email-reset-password'),
    url(r'^api/logout/$', logout_user, name='logout'),
    url(r'^api/login/$', login_user, name='login'),
    url(r'^api/room/action/(?P<pk>\d+)$', room_action, name='room_action_detail'),
    url(r'^api/room/$', create_show_room, name='create_show_room'),
    url(r'^api/change/password/$', change_password, name='change_user'),
    url(r'^api/update/user/$', update_info_instructor, name='change_user'),
    url(r'^api/quiz/action/(?P<pk>\d+)$', quiz_action, name='quiz_action'),
    url(r'^api/render/question/(?P<pk>\d+)$', render_question, name='render_question'),
    url(r'^api/filter/room/$', filter_room, name='filter_room'),
    url(r'^api/list/quiz$', filter_quiz, name='filter_quiz'),

    url(r'^QuizSys/', views.login_page, name='login_page'),
    url(r'^home/$', views.homepage, name='homepage'),
    url(r'^forgot/password$', forgot_password, name='forgot-password'),
    url(r'^404_page$', views.page_404, name='404_page'),
    url(r'^info/$', views.info_page, name='info_page'),
    url(r'^$', views.facebook, name='facebook')
]