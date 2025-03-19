from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework.decorators import action


class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

    @action(detail=False, methods=['POST'], url_path='by_ids')
    def by_ids(self, request):
        user_ids = request.data.get('ids', [])
        users = self.queryset.filter(id__in=user_ids)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

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