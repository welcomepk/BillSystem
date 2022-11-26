from .base import *
import environ
print("You are in Production")
env = environ.Env()
# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


SECRET_KEY = env('DJ_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

# db conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'billsystem',
        'USER': 'pk',
        'PASSWORD': env('DB_KEY'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
