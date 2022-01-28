"""
Django settings for API_CLIENTE project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ap5_370aeah755k2cwp@23q52&e@#=s4uyg559t^sk1f-)!7jw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [

    'adminlte3',
    'adminlte3_theme', 
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
       
    'bootstrap4',
    'sweetify',
    'crispy_forms',
    'django_tables2',
    'django_filters',
    #'aplicacao',
    'aplicacao.apps.AplicacaoConfig' 
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'API_CLIENTE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'API_CLIENTE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_cliente',
        'USER': 'root', 
        'PASSWORD': '', 
        'HOST': 'localhost', 
        'PORT': '3308', 
    },
    'Merchant': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uni_estoque',
        'USER': 'root', 
        'PASSWORD': 'root', 
        'HOST': 'localhost', 
        'PORT': '3306', 
    },
    'Smc_Light': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smc_automacao',
        'USER': 'root', 
        'PASSWORD': 'root', 
        'HOST': 'localhost', 
        'PORT': '3306', 
    }
}

# sweetify
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'  # usado durante o desenvolvimento
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # usado durante a produção

LOGOUT_REDIRECT_URL = 'login'
LOGOUT_URL = 'login'
LOGIN_REDIRECT_URL = '../aplicacao/index'

AUTH_USER_MODEL = 'aplicacao.CustomUsuario'