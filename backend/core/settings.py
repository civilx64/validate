"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import logging

from dotenv import load_dotenv
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-um7-^+&jbk_=80*xcc9uf4nh$4koida7)ja&6!vb*$8@n288jk"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)
DEVELOPMENT = os.environ.get('ENV', 'PROD').upper() in ('DEV', 'DEVELOP', 'DEVELOPMENT')
STAGING = os.environ.get('ENV', 'PROD').upper() in ('STAGE', 'STAGING', 'QA')
PRODUCTION = os.environ.get('ENV', 'PROD').upper() in ('PROD', 'PRODUCTION', 'PRD')
PUBLIC_URL = os.getenv('PUBLIC_URL').strip('/') if os.getenv('PUBLIC_URL') is not None else None

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost", "backend"]

if os.environ.get("DJANGO_ALLOWED_HOSTS") is not None:
    ALLOWED_HOSTS += os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",                       # CORS
    "rest_framework",                    # DRF
    "rest_framework.authtoken",
    "drf_spectacular",                   # OpenAPI/Swagger
    "drf_spectacular_sidecar",           # required for Django collectstatic discovery
    
    "django_celery_results",             # Celery result backend
    "django_celery_beat",                # Celery scheduled tasks

    "apps.ifc_validation",               # IfcValidation Service
    "apps.ifc_validation_models",        # IfcValidation Data Model
    "apps.ifc_validation_bff",           # IfcValidation ReactUI BFF

    "django_cleanup.apps.CleanupConfig"  # to automatically remove unlinked files
]

if DEVELOPMENT:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    #"django.middleware.gzip.GZipMiddleware",  # WE DO THIS IN NGINX
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = []
if os.environ.get("DJANGO_TRUSTED_ORIGINS") is not None:
    CORS_ALLOWED_ORIGINS += os.environ.get("DJANGO_TRUSTED_ORIGINS").split(" ")

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-requested-with',
    'x-csrf-token',
    'cache-control' # extra header
]

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRF_TOKEN'
CSRF_TRUSTED_ORIGINS = []
if os.environ.get("DJANGO_TRUSTED_ORIGINS") is not None:
    CSRF_TRUSTED_ORIGINS += os.environ.get("DJANGO_TRUSTED_ORIGINS").split(" ")

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'IFC Validation Service API',
    'DESCRIPTION': 'API for the buildingSMART Validation Service',
    'VERSION': os.environ.get("VERSION", "UNDEFINED"),
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',

    # OTHER SETTINGS
}

ROOT_URLCONF = "core.urls"

UI_TEMPLATES = os.path.join(BASE_DIR, 'templates') 
CORE_TEMPLATES = os.path.join(CURRENT_DIR, 'templates')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ UI_TEMPLATES, CORE_TEMPLATES ],
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

WSGI_APPLICATION = "core.wsgi.application"

# Used by DEBUG-Toolbar 
INTERNAL_IPS = [
    "127.0.0.1"
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DB_SQLITE = "sqlite"
DB_POSTGRESQL = "postgresql"

DATABASES_ALL = {
    DB_SQLITE: {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django_db.sqlite3",
    },
    DB_POSTGRESQL: {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "PORT": int(os.environ.get("POSTGRES_PORT", "5432")),
    },
}

DATABASES = {"default": DATABASES_ALL[os.environ.get("DJANGO_DB", DB_SQLITE)]}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "django_static/"
STATIC_ROOT = BASE_DIR / "django_static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Uploaded files
MAX_FILES_PER_UPLOAD = 100
MEDIA_URL = '/files/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/files_storage')
try:
    os.makedirs(MEDIA_ROOT, exist_ok=True)
except Exception as err:
    msg = "Configuration for MEDIA_ROOT is invalid: '{}' does not exist and could not be created ({})."
    raise ImproperlyConfigured(msg.format(MEDIA_ROOT, err))

# Celery broker, timers and result
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
#CELERY_RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", 'django-db')
CELERY_RESULT_BACKEND_DB = os.environ.get("CELERY_RESULT_BACKEND_DB", 'db+postgresql+psycopg2://postgres:postgres@db/postgres')
CELERY_CACHE_BACKEND = os.environ.get("CELERY_CACHE_BACKEND", 'django-cache')

CELERY_RESULT_EXTENDED = True
CELERY_TASK_SOFT_TIME_LIMIT = int(os.environ.get("CELERY_TASK_SOFT_TIME_LIMIT", 25*60))  # 25 min timeout per task
CELERY_TASK_TIME_LIMIT = int(os.environ.get("CELERY_TASK_SOFT_TIME_LIMIT", 30*60))  # 30 min timeout per task
CELERY_SEND_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = 90*24*3600 # Results in backend expire after 3 months

# reliability settings - see https://www.francoisvoron.com/blog/configure-celery-for-reliable-delivery
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_WORKER_STATE_DB = os.environ.get("CELERY_WORKER_STATE_DB", './celery-state')
try:
    os.makedirs(os.path.dirname(CELERY_WORKER_STATE_DB), exist_ok=True) 
except Exception as err:
    msg = "Configuration for CELERY_WORKER_STATE_DB is invalid: '{}' does not exist and could not be created ({})."
    raise ImproperlyConfigured(msg.format(os.path.dirname(CELERY_WORKER_STATE_DB), err))

CELERY_BEAT_SCHEDULE_FILENAME = os.environ.get("CELERY_BEAT_SCHEDULE_FILENAME", './celerybeat-schedule')
try:
    os.makedirs(os.path.dirname(CELERY_BEAT_SCHEDULE_FILENAME), exist_ok=True) 
except Exception as err:
    msg = "Configuration for CELERY_BEAT_SCHEDULE_FILENAME is invalid: '{}' does not exist and could not be created ({})."
    raise ImproperlyConfigured(msg.format(os.path.dirname(CELERY_BEAT_SCHEDULE_FILENAME), err))

# LOGGING

log_folder = os.getenv("DJANGO_LOG_FOLDER", "logs")
os.makedirs(log_folder, exist_ok=True)

LOGGING = {

    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "sql_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            # "formatter": "sql",
            "filename": os.path.join(log_folder, "sql.log"),
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_folder, "django.log"),
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "formatters": {
        "simple": {
            "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s',            
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] m:%(module)s pid:%(process)d tid:%(thread)d -- %(message)s'
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        # 'django.db.backends': {
        #     'handlers': ["sql_log"],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        "ifcvalidation": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    }
}

# Email
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'noreply@localhost')  # who to contact with questions/comments
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'noreply@localhost')      # who receives admin-style notifications

# IAM - Azure AD B2C
B2C_CLIENT_ID = os.environ.get("B2C_CLIENT_ID", None)
B2C_CLIENT_SECRET = os.environ.get("B2C_CLIENT_SECRET", None)
B2C_AUTHORITY = os.environ.get("B2C_AUTHORITY", None)
B2C_USER_FLOW = os.environ.get("B2C_USER_FLOW", None)

LOGIN_URL = os.environ.get("LOGIN_URL", f"{PUBLIC_URL}/login")
LOGOUT_URL = os.environ.get("LOGOUT_URL", f"{PUBLIC_URL}/logout")
LOGIN_CALLBACK_URL = os.environ.get("CALLBACK_URL", f"{PUBLIC_URL}/callback")
POST_LOGIN_REDIRECT_URL = os.environ.get("POST_LOGIN_REDIRECT_URL", f"{PUBLIC_URL}/dashboard")

AUTHLIB_OAUTH_CLIENTS = {
    'b2c': {
        'client_id': B2C_CLIENT_ID,
        'client_secret': B2C_CLIENT_SECRET,
        'server_metadata_url':f'{B2C_AUTHORITY}/{B2C_USER_FLOW}/v2.0/.well-known/openid-configuration',
        'client_kwargs': {'scope': 'openid profile email'}
    }
}
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')