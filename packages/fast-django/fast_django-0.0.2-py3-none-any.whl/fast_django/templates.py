from jinja2 import Template


class _Databases:
    name = "DATABASES"
    new = Template("""DATABASES = {
    'default': {
        'ENGINE': '{{database}}',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}""")


class _AsgiApplication:
    new = Template("""ASGI_APPLICATION = '{{project_name}}.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))],
        },
    },
}""")


class _Asgi:
    old = Template("""\nfrom django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{project_name}}.settings')

application = get_asgi_application()""")

    new = Template("""from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from some_app import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{project_name}}.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})""")


class _AppUrls:
    new = Template("""from django.urls import path
from .views import *

app_name = '{{app_name}}'

urlpatterns = [
    # path('example/', example, name='example'),
]""")


class _Templates:
    name = "TEMPLATES"
    new = """TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]"""


class _Languages:
    new = """LANGUAGES = [
    ('en', 'English'),
    ('zh-hans', '中文（简体）'),
]"""


class _Accounts:
    new = Template("""LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/{{app_name}}/login/'

AUTH_USER_MODEL = '{{app_name}}.CustomUser'""")


class _RestFramework:
    new = """REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}"""


class _Serializer:
    new = Template("""from rest_framework import serializers
from {{app_name}}.models import *""")


class T:
    Databases = _Databases
    AsgiApplication = _AsgiApplication
    Asgi = _Asgi
    AppUrls = _AppUrls
    Templates = _Templates
    Languages = _Languages
    Accounts = _Accounts
    RestFramework = _RestFramework
    Serializer = _Serializer
