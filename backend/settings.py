"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changemeplease")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "PRODUCTION" not in os.environ
PROD = False

if not DEBUG:
    print("[INFO] We are in PRODUCTION mode")
    PROD = True
else:
    print("[INFO] We are in DEBUG mode")

ALLOWED_HOSTS = ["localhost"]

EXTERNAL_HOSTNAME = os.environ.get("EXTERNAL_HOSTNAME")
if EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(EXTERNAL_HOSTNAME)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}


# This allows us to override the User Model
AUTH_USER_MODEL = "users.User"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party Apps
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "corsheaders",
    "storages",
    # Local Apps
    "users",
    "teams",
    "links",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Uncomment for desired authentication method
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'django.contrib.auth.backends.ModelBackend',
        "rest_framework.authentication.TokenAuthentication"
    ]
}

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# PostGreSQL Database Setup
if PROD:
    DATABASES = {}
    db_from_env = dj_database_url.config(conn_max_age=300, ssl_require=True)
    DATABASES["default"] = db_from_env
else:
    # SQLite Database Setup
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
    # PostgreSQL Config
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql_psycopg2",
    #         "NAME": os.environ.get("DB_NAME", ""),
    #         "USER": os.environ.get("DB_USER", ""),
    #         "PASSWORD": os.environ.get("DB_PASS", ""),
    #         "HOST": "localhost",
    #         "PORT": "5432",
    #     }
    # }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# AWS Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'


if not DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory in production
    # STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    # For media files, use the default Django storage backend.
    # DEFAULT_FILE_STORAGE = 'backend.storage.MediaStorage' 
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CORS_ALLOWED_ORIGINS = [
    # TODO: Add the frontend URL here
]

CORS_ALLOW_ALL_ORIGINS = DEBUG

BRANDFETCH_API_TOKEN = os.environ.get("BRANDFETCH_API")


