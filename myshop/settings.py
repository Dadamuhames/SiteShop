import os
from pathlib import Path

#from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gti+5u3@zx(q^qki%urii*!^=js7uj-qzj*(w7qxog7ovryazx'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main', 'cart', 'account',
    'rest_framework', 'palpay', 'django_filters',
    'easy_thumbnails',  'paycomuz',
    'admins', 'colorfield',
]

#'social_django',

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['main/templates', 'account/templates'],
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
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '110430500482-pseofk25u9bo7n2tils1cok5cqg39nds.apps.googleusercontent.com'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#LOGIN_URL = '/accounts/complete/telegram'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = '5691196380:AAGVb2EAjuE_FAxm3o8hPv5ils1a5GGpOE8'

#You can use this token to access HTTP API:
#

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'main', 'static'),
    os.path.join(BASE_DIR, 'account', 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' for sever
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dadamuhames@gmail.com'
EMAIL_HOST_PASSWORD = 'iwibjvzyvbaioxuo'
EMAIL_PORT = 588
EMAIL_USE_SSL = False
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SSL_CERTFILE = 'main'
EMAIL_SSL_KEYFILE = 'main'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'
    )
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 10,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    },
    'cart': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}


THUMBNAIL_ALIASES = {
    '': {
        'product_img': {'size': (400, 400), 'crop': False},
        'cart': {'size': (200, 200), 'crop': False},
        'prod_photo': {'size': (600, 600), 'crop': False},
        'btn_img': {'size': (50, 50), 'crop': False},
        'avatar': {'size': (90, 90), 'crop': False}
    },
}


PAYCOM_SETTINGS = {
    "KASSA_ID": "63552532f72e1b58066a81bd",  # token
    "SECRET_KEY": "tCF9?fEv8oYZT9RY7Hkh&eQm8PYXQUVbqokv",  # password
    "ACCOUNTS": {
        "KEY": "order_id"
    },
    'TOKEN': ''
}

