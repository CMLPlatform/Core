"""
Django settings for CMLMasterProject project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# location of manage.py
BASE_DIR = os.path.dirname(os.path.dirname
                           (os.path.dirname(os.path.abspath(__file__))))
# location of settings.py
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__)),
)


# create the actual template link to tell the project were the template is
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

# get the static directory for images etc
STATIC_PATH = os.path.join(BASE_DIR, 'static_assets')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    STATIC_PATH,
    os.path.join(BASE_DIR, 'assets'),

)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PUMA',
    'leaflet',
    'djgeojson',
    'bootstrapform',
    'CMLMasterProject',
        #wigtail CMS apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    #'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    # panorama
    'panorama',
    # circumat and dependencies
    'circumat',
    'channels',
    'django_celery_results',
    'modelcluster',
    'taggit',
    'CMS',
    "wagtail.contrib.table_block",
    'MicroVis',
    'widget_tweaks',
    'rest_framework',
    # 'snippets.apps.SnippetsConfig',
    'webpack_loader'

]

redis_host = os.environ.get('REDIS_HOST', 'localhost')
# Channels settings
CHANNEL_LAYERS = {
    "default": {
        # The Redis channel layer implementation channels_redis
        "BACKEND":
            "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
        },
    },
}
# ASGI_APPLICATION should be set to your outermost router
ASGI_APPLICATION = 'CMLMasterProject.routing.channel_routing'

# Celery config
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
# as the calculations are CPU and MEM intensive,
# enforce a new worker after a task is finished to release memory
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # wigtail CMS
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'CMLMasterProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
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

WSGI_APPLICATION = 'CMLMasterProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DATABASES_DEFAULT_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SECURITY WARNING: keep the secret keys used in production secret!
AUTHENTICATION_KEY_RESEARCH = 'my_authentication_key'
AUTHENTICATION_KEY_STUDENT = 'my_authentication_key'
# disable authentication for DRF for now
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': []
}
#PUMA CONFIGURATIONS
LEAFLET_CONFIG = {

 #  'SPATIAL_EXTENT': (4.9597, 52.4551, 4.9, 52.3372),


#'MINIMAP': True,
    'ATTRIBUTION_PREFIX': 'Powered by django-leaflet & IE-SoftLab',

   #'RESET_VIEW': False
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
#above defines where media files uploaded should be stored

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

#login -> redirect to home
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
#for server !!
#LOGIN_REDIRECT_URL = '/platform/' -> THIS MIGHT NOT BE NEEDED ANYMORE SO USE '/' DIRECTLY
#wagtail site name of dashboard admin
WAGTAIL_SITE_NAME = 'CML\'s'