from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SITE_URL = 'http://127.0.0.1:8000'
# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-q0-!6c4228evgasyo%nl828#-p*a+yr(bw!8znp-!+vfgv3@yf'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

LOGIN_REDIRECT_URL = '/'  # URL to redirect to after successful login
LOGOUT_REDIRECT_URL = '/'  # URL to redirect to after logout

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'events', 'templates', 'events')],  # Ensure this path is correct
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

WSGI_APPLICATION = 'event_management_system.wsgi.application'

# Database settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'eventhub_database',
#         'USER': 'alvinroot',
#         'PASSWORD': 'Alvin200115',
#         'HOST': 'eventhub-database.czsgiywaiemw.eu-north-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST',),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
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

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Default language set to U.S. English
TIME_ZONE = 'Asia/Kolkata'  # Time zone set to Indian Standard Time (IST)
USE_I18N = True  # Enable Django's internationalization system
USE_TZ = True  # Enable timezone-aware datetime handling


# # Static files (CSS, JavaScript, Images)
# # Use S3 for static files in production
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # S3 bucket for static files
# AWS_STATIC_CUSTOM_DOMAIN = 'eventhub-static.s3.amazonaws.com'  # Ensure the bucket name is 'eventhub-static' for static files
# STATIC_URL = f'https://{AWS_STATIC_CUSTOM_DOMAIN}/static/'

# # Media files (Uploads)
# AWS_S3_CUSTOM_DOMAIN = 'eventhub-media.s3.amazonaws.com'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# # Remove this because media files are stored on S3, not on the local filesystem
# # MEDIA_ROOT is unnecessary when using S3 for media files
# # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # AWS Credentials and S3 settings
# AWS_ACCESS_KEY_ID = 'AKIAQPHJMQZMA3V7K7UD'
# AWS_SECRET_ACCESS_KEY = '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'

# # S3 bucket for media files (ensure this bucket is set up for media files)
# AWS_STORAGE_BUCKET_NAME = 'eventhub-media'
# AWS_S3_REGION_NAME = 'eu-north-1'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None  # Set ACL to None (files will be private by default)
# AWS_S3_VERIFY = True

# # S3 Object Parameters (Cache-Control)
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# # Use S3 for media storage
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')  # e.g., 'us-east-1'
AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION')


# S3 bucket configuration
AWS_S3_CUSTOM_DOMAIN = f'eventhub-storage.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# # Media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Email settings
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Fetch from .env
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Fetch from .env
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')  # Default from email

