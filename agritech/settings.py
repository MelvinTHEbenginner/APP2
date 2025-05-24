# Configuration pour l'envoi d'emails
# settings.py
import os
from dotenv import load_dotenv
load_dotenv()
# settings.py (configuration corrigée)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587  
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = os.getenv('GMAIL_EMAIL') 
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'emmanuelgmc123@gmail.com'  

from pathlib import Path 
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^qk%@d0p*fd-n187m#^wgn4)vonvx0^a5@lp*f9q#s91nxam7a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'agritech_app',  # Your app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.timezone.TimezoneMiddleware'
]

ROOT_URLCONF = 'agritech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': ['templates'],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'agritech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# settings.py

LANGUAGE_CODE = 'fr'

LANGUAGES = [
    ('fr', 'Français'),
    ('ak', 'Akan'),  # Exemple de langue locale
    ('wo', 'Wolof'), # Autre exemple
    # Ajoutez d'autres langues locales pertinentes pour la Côte d'Ivoire
]

TIME_ZONE = 'Africa/Abidjan'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redirection après connexion
#LOGIN_REDIRECT_URL = 'home'  # Redirige vers la page d'accueil après connexion
LOGIN_URL = 'login'           # URL de la page de connexion
LOGOUT_REDIRECT_URL = 'home'  # Redirige vers la page d'accueil après déconnexion
LOGIN_REDIRECT_URL = 'profile'  # Rediriger vers le profil après connexion
LOGIN_URL = 'login'