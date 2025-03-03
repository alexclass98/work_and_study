from django.contrib import admin
from django.urls import path, include
from was_app import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.AuthUserViewSet)
router.register(r'form', views.UserFormViewSet)
router.register(r'user-skill', views.UserSkillViewSet)
router.register(r'skills', views.SkillsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
