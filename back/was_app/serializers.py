from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

User = get_user_model()

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForm
        fields = '__all__'


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cources
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class UserSkillFilter(filters.FilterSet):
    pass
    user_id = filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    skill_id = filters.NumberFilter(field_name='skill_id', lookup_expr='exact')

    class Meta:
        model = UserSkill
        fields = ['user_id', 'skill_id']