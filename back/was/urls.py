from django.contrib import admin
from django.urls import path, include, re_path

from was import consumers
from was_app import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.AuthUserViewSet, basename='users')
router.register(r'form', views.UserFormViewSet, basename='form')
router.register(r'user-skill', views.UserSkillViewSet)
router.register(r'skills', views.SkillsViewSet)
router.register(r'messages', views.MessagesViewSet)
router.register(r'cources', views.CourcesViewSet)


urlpatterns = [
# WebSocket
    re_path(r'^ws/wall/$', consumers.WallConsumer.as_asgi()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
