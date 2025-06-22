from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#lgd+tdbnjcz00th--^bg@-n56o$y+3esspag5uki@g@up!hpb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'restaurant.apps.RestaurantConfig',
    
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'jwt': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'SWAGGER_UI_REQUEST_HEADERS': [
        {
            'name': 'Authorization',
            'description': 'JWT Token',
            'value': 'Bearer <your_jwt_token_here>'
        },
    ],
    'LOGIN_URL': 'api/v1/auth/login',
    "DEFAULT_MODEL_RENDERING": "example"
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'authe.custom_jwt.CustomJWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14)
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'restaurant.CustomUser'

JAZZMIN_SETTINGS = {
    "site_title": "My Admin Panel",
    "site_header": "My Project Admin",
    "site_brand": "My Admin",
    # "site_logo": "myapp/logo.png",  # static fayldagi logotip (bo‘lsa)
    "welcome_sign": "Welcome to My Admin Panel",
    "copyright": "My Company © 2025",
    "search_model": ["auth.User", "myapp.MyModel"],

    # Yon panel bo‘limlari tartibi
    "order_with_respect_to": ["auth", "myapp"],

    # Sidebar collapse bo‘lishini xohlaysizmi?
    "navigation_expanded": False,
    
    # Bo'limlar uchun maxsus piktogrammalar
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },

    # Custom menyu (istasa)
    # "custom_links": {
    #     "auth": [{
    #         "name": "Custom link",
    #         "url": "https://google.com",
    #         "icon": "fas fa-link",
    #         "permissions": ["auth.view_user"]
    #     }]
    # },
}
