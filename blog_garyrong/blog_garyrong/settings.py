#coding:utf-8
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from platform import platform
if 'centos' in platform():
    DEBUG = False
else:
    DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iajet=_uw0dvr4a%v-n-odngyteh5ok3yspl-xw*h=+a+(0sk^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    # extensive app
    'xadmin',
    'crispy_forms', # xadmin's dependency
    'reversion',
    'duoshuo', # comment plugin
)
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', # enable gzip compression
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ("debug_toolbar.middleware.DebugToolbarMiddleware",)

ROOT_URLCONF = 'blog_garyrong.urls'

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'template').replace('\\','/')],
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

WSGI_APPLICATION = 'blog_garyrong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Database Settting
if DEBUG:
    DOMAIN = "http://localhost:8000"
    DB_NAME = "garyrong.sqlite3"
    DB_USER = "root"
    DB_PWD = "root"
else:
    DOMAIN = "http://www.garyrong.cn"
    DB_NAME = "mydb"
    DB_USER = "garyrong"
    DB_PWD = "rjl88387132"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_NAME,
        "USER" : DB_USER,
        "PASSWORD" : DB_PWD,
        "HOST" : "",
        "PORT" : "",

    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder' # django will look for static file in the application directory
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Log Setting
if DEBUG:
    LOG_FILE = '/tmp/blog.log'
else:
    LOG_FILE = '/home/garyrong/virtualenvs/blog/logs/all.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(module)s : %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s : %(message)s'
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILE,
            'mode': 'a',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
# End Log Setting


# Cache Setting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}
# End Cache Setting

# Basic Common Setting
PAGE_NUM = 8
RECENTLY_NUM = 5
HOT_NUM = 5
LIKE_MOST_NUM = 5
ONE_DAY = 24*60*60
FIF_MIN = 15 * 60
FIVE_MIN = 5 * 60

DUOSHUO_SECRET = 'b676a6b61e307243240d4dc7dfc68c2d'
DUOSHUO_SHORT_NAME = 'garyrong'

# 微信
WEIXIN_APPID = 0
WEIXIN_APPSECRET = ''
# End Basic Common Setting

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_URL = '/static/'


