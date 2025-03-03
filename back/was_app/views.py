from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import *
from .models import *


class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

class UserFormViewSet(viewsets.ModelViewSet):
    queryset = UserForm.objects.all()
    serializer_class = UserFormSerializer


class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


class UserSkillViewSet(viewsets.ModelViewSet):
    # Описание класса лекарств, добавляем тут сериалайзер и поля для фильтрации
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer

class CourcesViewSet(viewsets.ModelViewSet):
    # Описание класса лекарств, добавляем тут сериалайзер и поля для фильтрации
    queryset = Cources.objects.all()
    serializer_class = CoursesSerializer

class MessagesViewSet(viewsets.ModelViewSet):
    # Описание класса лекарств, добавляем тут сериалайзер и поля для фильтрации
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer