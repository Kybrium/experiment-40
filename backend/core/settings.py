import os
import sys
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


# ========== INITS ==========
load_dotenv()
# ===========================


# ========== PROJECT META ==========
PROJECT_NAME = "Experiment 40"
# ==================================


# ========== MAIN SETTINGS ==========
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DJANGO_DEBUG", os.getenv("DJANGO-DEBUG", "true")).lower() == "true"
HOSTS = os.getenv("DJANGO_HOSTS", "localhost,127.0.0.1").split(",")
HOSTS_URLS = os.getenv("DJANGO_HOSTS_URLS","http://localhost:3000,http://127.0.0.1:3000").split(",")
ALLOWED_HOSTS = HOSTS
CORS_ALLOWED_ORIGINS = HOSTS_URLS
CSRF_TRUSTED_ORIGINS = HOSTS_URLS
CORS_ALLOW_CREDENTIALS = True
MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE') == 'True'
# ===================================


# ========== DEFINITION ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_otp',
    'django_otp.plugins.otp_totp',

    'accounts',
    'infrastructure',
    'minecraft',
]

MIDDLEWARE = [
    'infrastructure.middlewares.MaintenanceModeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'infrastructure.middlewares.UserLanguageMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'
# ================================


# ========== DATABASE ==========
DEFAULT_SQLITE_PATH = Path(__file__).resolve().parent.parent / "db.sqlite3"
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=60,
        )
    }
    if DATABASES["default"]["ENGINE"].endswith("mysql"):
        DATABASES["default"].setdefault("OPTIONS", {})
        DATABASES["default"]["OPTIONS"].update({
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'",
        })
else:
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
    if DB_ENGINE == "mysql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("DB_NAME", "exp40"),
                "USER": os.getenv("DB_USER", "exp40"),
                "PASSWORD": os.getenv("DB_PASSWORD", "exp40"),
                "HOST": os.getenv("DB_HOST", "db"),
                "PORT": int(os.getenv("DB_PORT", "3306")),
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "init_command": "SET sql_mode='STRICT_ALL_TABLES'",
                },
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": DEFAULT_SQLITE_PATH,
            }
        }

CONN_MAX_AGE = 60
# ==============================


# ========== LOGGER ==========
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
DJANGO_LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] | %(message)s "
    "(%(filename)s:%(lineno)d)"
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "console": {
            "format": DJANGO_LOG_FORMAT,
            "datefmt": "%d.%m.%Y %H:%M:%S",
        }
    },

    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "console",
        },
    },

    "loggers": {
        "core": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.db.backends": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },

    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}
# ============================


# ========== AUTH ==========
AUTH_USER_MODEL = 'accounts.User'

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

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.auth.CookieJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "SIGNING_KEY": SECRET_KEY,
}
# ==========================


# ========== INTERNATIONALIZATION (I18N) ==========
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "accounts" / "locale",
    BASE_DIR / "core" / "locale",
]
# ==========================================


# ========== STATIC & FILES ==========
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# ====================================


# ========== MODEL & DB DEFAULTS ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# =========================================


# ========== RUN MESSAGE ==========
try:
    from core.startup import print_startup_banner
    print_startup_banner(sys.modules[__name__])
except Exception:
    print(Exception)
# =================================