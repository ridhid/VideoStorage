#coding: utf-8
# Django settings for camsViewer project.

import os
import sys

#решает проблемы с выводом латиницы
reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'local.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#  MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'third_party', 'components'),
    os.path.join(PROJECT_ROOT, 'static'),
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder'
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'third_party')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+-bplf9jtru6x@1x0sfno&k1fbdeqw)*$#u#86#m4@#%furv(u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'camsViewer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'camsViewer.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    ##########
    'south',
    # 'djangobower',
    #########
    'apps.fs',
    'apps.main',
    'apps.server',
    'apps.cameras',
)

BOWER_INSTALLED_APPS = (
    'jquery',
    'knockout',
    'sammy',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# # active directory authentication module
# AD_DNS_NAME = 'orenmfc.ru' # FQDN of your DC If using non-SSL use these
# #AD_LDAP_PORT=389
# #AD_LDAP_URL='ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
# # If using SSL use these:
# AD_LDAP_PORT=636
# AD_LDAP_URL='ldaps://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
#
# AD_SEARCH_DN = 'dc=orenmfc,dc=ru'
# AD_NT4_DOMAIN = 'ORENMFC.RU'
# AD_SEARCH_FIELDS = ['mail','givenName','sn','sAMAccountName','memberOf']
# AD_MEMBERSHIP_ADMIN = ['Domain Admins', 'Administrators', 'Enterprise Admins']   # this ad group gets superuser status in django
# AD_MEMBERSHIP_REQ = AD_MEMBERSHIP_ADMIN + ['Video']    # only members of this group can access
# AD_CERT_FILE = '%s/cerificate.pem' % os.getcwd() # this is the certificate of the Certificate Authority issuing your DCs certificate
# AD_DEBUG=False
# AD_DEBUG_FILE='%s/ldap.debug' % os.getcwd()
#
# AUTHENTICATION_BACKENDS = (
#     'camsViewer.ad_backend.ActiveDirectoryAuthenticationBackend',
#     'django.contrib.auth.backends.ModelBackend'
# )


LOGIN_REDIRECT_URL = '/'


# CAMS_SERVER_SETTINGS_FILE = 'config.test'
CAMS_SERVER_SETTINGS_FILE = '/home/user/video_server/config.cfg'

VIDEO_ROOT = '/home/user/camera'
# VIDEO_ROOT = '/home/ridhid/'
VIDEO_URL_PREFIX = '/media/'
# VIDEO_URL_PREFIX = '/file?file='