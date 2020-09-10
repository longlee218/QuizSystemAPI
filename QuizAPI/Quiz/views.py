from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import organization_type_data

def login_page(request):
    return render(request, 'Quiz/index.html')


@permission_classes([IsAuthenticated])
def homepage(request):
    context = {'username': request.user}
    return render(request, 'Quiz/homepage.html', context)


def page_404(request):
    return render(request, 'Quiz/404.html')


def facebook(request):
    return render(request, 'Quiz/facebook.html')


@permission_classes([IsAuthenticated])
def info_page(request):
    context = {
        'organization_type': organization_type_data
    }
    return render(request, 'Quiz/info_page.html', context)


@permission_classes([IsAuthenticated])
def reset_password(request):
    return render(request, 'Quiz/reset_password.html', context={})