import os

from pathlib import Path
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.getenv("DEBUG")) == "1"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    # "social_django",
    "rest_framework",
    "rest_framework_jwt",
    # Application
    "users",
    "authentication",
    "tweets",
]

# apiexample/settings.py

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}

# apiexample/settings.py

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentication.middleware.AuthorizationMiddleware"
]

# apiexample/settings.py

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# AUTHENTICATION_BACKENDS = {
#     "authentication.auth_backend.Auth0",
#     "django.contrib.auth.backends.ModelBackend",
# }

LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/dashboard"

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Twitter api credentials

TWITTER_API_KEY = str(os.getenv("TWITTER_API_KEY"))
TWITTER_API_SECRET_KEY = str(os.getenv("TWITTER_API_SECRET_KEY"))
TWITTER_ACCESS_TOKEN = str(os.getenv("TWITTER_ACCESS_TOKEN"))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

TWITTER_API_BEARER_TOKEN = str(os.getenv("TWITTER_API_BEARER_TOKEN"))

TWITTER_API_BASE_URL = str(os.getenv("TWITTER_API_BASE_URL"))
TWITTER_API_BASE_URL_V1 = str(os.getenv("TWITTER_API_BASE_URL_V1"))

OAUTH_NONCE = str(os.getenv("OAUTH_NONCE"))

OAUTH_CLIENT_ID = str(os.getenv("OAUTH_CLIENT_ID"))
OAUTH_CLIENT_SECRET = str(os.getenv("OAUTH_CLIENT_SECRET"))
OAUTH_REDIRECT_URI = str(os.getenv("OAUTH_REDIRECT_URI"))


# Auth0 settings
# SOCIAL_AUTH_TRAILING_SLASH = False
SOCIAL_AUTH_AUTH0_DOMAIN = str(os.getenv("AUTH0_DOMAIN"))
SOCIAL_AUTH_AUTH0_AUDIENCE = str(os.getenv("AUTH0_API_AUDIENCE"))
SOCIAL_AUTH_AUTH0_API_TOKEN = str(os.getenv("AUTH0_API_TOKEN"))
SOCIAL_AUTH_AUTH0_KEY = str(os.getenv("AUTH0_CLIENT_ID"))
SOCIAL_AUTH_AUTH0_SECRET = str(os.getenv("AUTH0_CLIENT_SECRET"))


# webappexample\settings.py
SOCIAL_AUTH_AUTH0_SCOPE = ["openid", "profile", "email"]

# CORS settings
CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "localhost:3000",
]
CSRF_COOKIE_SAMESITE = None

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "authentication.utils.jwt_get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "authentication.utils.jwt_decode_token",
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": "https://django-twitter2.0/api",
    "JWT_ISSUER": SOCIAL_AUTH_AUTH0_DOMAIN,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}
