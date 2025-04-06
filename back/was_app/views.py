from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework.decorators import action
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from was.consumers import WallConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserSkillFilter
    search_fields = ['^user_id', '^skill_id']

class CourcesViewSet(viewsets.ModelViewSet):
    # Описание класса лекарств, добавляем тут сериалайзер и поля для фильтрации
    queryset = Cources.objects.all()
    serializer_class = CoursesSerializer

class MessagesViewSet(viewsets.ModelViewSet):
    # Описание класса лекарств, добавляем тут сериалайзер и поля для фильтрации
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def perform_create(self, serializer):
        # Сохраняем сообщение, как обычно, но получаем созданный экземпляр
        # Убедитесь, что author устанавливается правильно (автоматически из request.user или передан)
        # Если автор не устанавливается автоматически, его нужно добавить:
        # message_instance = serializer.save(author=self.request.user)
        message_instance = serializer.save()  # Сохраняем

        # Сериализуем созданное сообщение снова, чтобы получить все поля (включая ID, date_send)
        # Важно использовать тот же сериализатор, что и для API
        serialized_message = MessagesSerializer(message_instance).data

        # Отправляем событие в группу WebSocket через слой каналов
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            WallConsumer.GROUP_NAME,  # Имя группы из консьюмера
            {
                'type': 'wall.message',  # Это вызовет метод wall_message в консьюмере
                'message': serialized_message  # Передаем данные созданного сообщения
            }
        )
        print(f"Sent message {message_instance.id} to channel group {WallConsumer.GROUP_NAME}")
