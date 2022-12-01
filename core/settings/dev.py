from .base import *
print("You are in devolopment")
SECRET_KEY = 'django-insecure-f=f^_2l=!@qy@@$*4w5gqvo&k5oli288**d2+p39s11kcgxy-&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
