import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'was.settings')  # Замените your_project_name на имя вашего проекта
django.setup()

from was_app.models import Skills, AuthUser, UserForm, UserSkill, Cources, Messages

def create_test_data():
    # Получаем существующих пользователей
    user1 = AuthUser.objects.get(username='222')
    user2 = AuthUser.objects.get(username='333')

    # Создание навыков (если они ещё не созданы)
    if not Skills.objects.filter(skill_name='Python').exists():
        Skills.objects.create(type=True, skill_name='Python', category='Programming', test='Python Test')
    if not Skills.objects.filter(skill_name='Communication').exists():
        Skills.objects.create(type=False, skill_name='Communication', category='Soft Skills', test='Communication Test')
    if not Skills.objects.filter(skill_name='JavaScript').exists():
        Skills.objects.create(type=True, skill_name='JavaScript', category='Programming', test='JavaScript Test')
    if not Skills.objects.filter(skill_name='Teamwork').exists():
        Skills.objects.create(type=False, skill_name='Teamwork', category='Soft Skills', test='Teamwork Test')

    # Получаем навыки
    python_skill = Skills.objects.filter(skill_name='Python').first()
    communication_skill = Skills.objects.filter(skill_name='Communication').first()
    javascript_skill = Skills.objects.filter(skill_name='JavaScript').first()

    # Создание или обновление форм пользователей
    user_forms = [
        {'user_id': user1, 'gender': True, 'city': 'Moscow', 'country': 'Russia', 'dd_mm_yy': '1990-01-01', 'surname': 'Doe', 'middlename': 'A.'},
        {'user_id': user2, 'gender': False, 'city': 'New York', 'country': 'USA', 'dd_mm_yy': '1995-05-05', 'surname': 'Doe', 'middlename': 'B.'},
    ]
    for form_data in user_forms:
        user_form, created = UserForm.objects.get_or_create(
            user_id=form_data['user_id'],
            defaults=form_data
        )
        if not created:
            # Если запись уже существует, обновляем её
            for key, value in form_data.items():
                setattr(user_form, key, value)
            user_form.save()

    # Создание навыков пользователей
    user_skills = [
        {'user_id': user1, 'skill_id': python_skill, 'level': 5},
        {'user_id': user2, 'skill_id': communication_skill, 'level': 3},
    ]
    for skill_data in user_skills:
        UserSkill.objects.create(**skill_data)

    # Создание курсов
    courses = [
        {'name': 'Python Basics', 'skill': python_skill, 'difficulty': 3, 'description': 'Learn Python from scratch', 'duration_hrs': 10},
        {'name': 'Effective Communication', 'skill': communication_skill, 'difficulty': 2, 'description': 'Improve your communication skills', 'duration_hrs': 8},
        {'name': 'Advanced JavaScript', 'skill': javascript_skill, 'difficulty': 4, 'description': 'Master JavaScript', 'duration_hrs': 12},
    ]
    for course_data in courses:
        Cources.objects.create(**course_data)

    # Создание сообщений
    messages = [
        {'parent_message_id': 0, 'author': user1, 'topic': 'Python Help', 'text': 'I need help with Python.'},
        {'parent_message_id': 1, 'author': user2, 'topic': 'Re: Python Help', 'text': 'I can help you with Python.'},
        {'parent_message_id': 0, 'author': user1, 'topic': 'JavaScript Question', 'text': 'How to use closures in JavaScript?'},
    ]
    for message_data in messages:
        Messages.objects.create(**message_data)

    print("Тестовые данные созданы!")

if __name__ == '__main__':
    create_test_data()