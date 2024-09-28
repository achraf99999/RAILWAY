"""
Django settings for image_noise_project project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
import environ
from environ import Env
import os
env = Env ()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')
# Feature Toggle
DEVELOPER = env('DEVELOPER', default='')
STAGING = env('STAGING', default='False')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# This will read the .env file if it's present
SECRET_KEY = env('SECRET_KEY')
ENCRYPT_KEY = env('ENCRYPT_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
   DEBUG = True
else:
   DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ 'localhost', '127.0.0.1', 'railway-production-18fb.up.railway.app' ]

CSRF_TRUSTED_ORIGINS = [ 'https://railway-production-18fb.up.railway.app' ]
INTERNAL_IPS = (
'127.0.0.1',
'loca lhost: 8000')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'image_noise',

]




MIDDLEWARE = [    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'image_noise_project.urls'

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

AUTHENTICATION_BACKENDS = [
'django. contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends. AuthenticationBackend',]

WSGI_APPLICATION = 'image_noise_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
     'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',}
}


POSTGRES_LOCALLY = False
if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
   DATABASES ['default'] = dj_database_url.parse(env('DATABASE_URL' )) 
   print(f"DATABASE_URL: {env('DATABASE_URL')}")  # Debug print to verify URL


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
