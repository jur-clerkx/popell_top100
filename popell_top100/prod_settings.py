from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "popell_top100",
        "USER": "postgres",
    }
}

DEBUG = False
SECURE_SSL_REDIRECT = True
SECRET_KEY = "nvj1!%2jekp83*yy@1m%(@d5!)+2=!jh&z-p0k8m0f!+z!pi1p"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
