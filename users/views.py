from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer


class ApiUserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCRMView(View):
    pass
