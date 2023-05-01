import os
from os.path import join
from pathlib import Path

from django.contrib import staticfiles

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o@2)fbmz8_wcp_)usyi0x@%!s2_801ezf#+=wcc8ghsrxs$c9z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Pour avoir accès sur le serveur local , on met l'ipV4 de la machine ici et on met le port 8000
# on fait python manage.py runserver l'ipV4:8000
ALLOWED_HOSTS = ['172.20.210.128', "localhost", "127.0.0.1", "192.168.1.101"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    "memberships",
    'my_ai',
    'fontawesomefree',
    'widget_tweaks',
    "django_htmx",
    'tinymce',
    'adpilot',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",

]

ROOT_URLCONF = 'answer_ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'answer_ai.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'impleai',
        'USER': 'nouhan',
        'PASSWORD': 'ET18008',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "my_ai/static"),
]

STATIC_URL = '/static/'
STATIC_ROOT = '/staticfiles/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/mediafiles/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'accounts.backends.CaseInsensitiveModelBackend',
)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# SMTP CONFIGURATION
"""EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'impleaiservice@gmail.com'
EMAIL_HOST_PASSWORD = 'ET18008gmailET18008!'"
"""

# STRIPE
STRIPE_SECRET_KEY = "sk_test_51LkES1Lzd8UZxNhh29YM4t224Zhqs9PmAiZgPYTf42btC3z9J10gWJcu5npvBr3x7FBEfdIEu0X9E9YFSRVk92TO00rTUBuZxk"
STRIPE_PUBLISHABLE_KEY = "pk_test_51LkES1Lzd8UZxNhhCe8T95HO2JQI8EUgfT9tqkPxXTiImskC2ZcoE1BLET8rQzhyicVgF8u9HOxQkV4sm4z5dw9C00gOCkrPjG"
WEBHOOK_ENDPOINT_SECRET = 'whsec_88daf7950fde3c019607ddd4630e3b384aa6790a4ac397170bfcabba1ece5668'

FACEBOOK_APP_ID = '1222527255134214'
FACEBOOK_APP_SECRET = "a54b2ad80651d5640101145f9f19b869"
FACEBOOK_ACCESS_TOKEN = "EAARX4c7FQAYBAEhcK7Ck5NqjiyMJ8FLiCuGMHbAaZAdZALwWoJwZB07VXA5KMBXqO7VSlTfIFToLBfG1NOR1pS9filOW74wajm8hvkWClbjjOQ2CT1pgyzEFittpP4fy5FNhOL1Gv7xbkdaiqfoPTz0NeE32knIE2Qy9AsMMPlkJOg0zhIpL20iAE3MItE753HHZC8uZARA0q58PGlez5R7EXGjuO2XZCXU9aZCUe6CvzJmj99u07Htk1Y2FjtHgAQZD"

# # TINYMCE
#
# TINYMCE_DEFAULT_CONFIG = {
#     "theme": "silver",
#     "height": 500,
#     "menubar": False,
#     "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
#                "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
#                "code,help,wordcount",
#     "toolbar": "undo redo | formatselect | "
#                "bold italic backcolor | alignleft aligncenter "
#                "alignright alignjustify | bullist numlist outdent indent | "
#                "removeformat | help",
# }
