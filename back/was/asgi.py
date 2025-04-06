# was/asgi.py

import os
# import django # Можно добавить для явного вызова setup, но get_asgi_application обычно достаточно
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# НЕ ИМПОРТИРУЕМ was.routing ЗДЕСЬ

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'was.settings')

# --- СНАЧАЛА инициализируем Django ASGI приложение ---
# Это настроит settings и приложения Django перед тем, как мы импортируем наш роутинг
django_asgi_app = get_asgi_application()
# Альтернатива (менее стандартная для ASGI, но рабочая):
# django.setup()

# --- ТЕПЕРЬ импортируем наш роутинг ---
import was.routing # Импорт ПОСЛЕ инициализации Django

# --- Собираем итоговое ASGI приложение ---
application = ProtocolTypeRouter({
    "http": django_asgi_app, # Используем уже инициализированное приложение
    "websocket": AuthMiddlewareStack(
        URLRouter(
            was.routing.websocket_urlpatterns
        )
    ),
})