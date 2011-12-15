# Django settings for labmachine project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1&i2*r*w8#$fu)87+3i5=sb#5d_9v4p^l&6lks+t6z$4x1m_%+'

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

ROOT_URLCONF = 'labmachine.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django_extensions',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'labmachine.apps.branch',
)

# Tell django to use celery
INSTALLED_APPS += ('djcelery',)
import djcelery
djcelery.setup_loader()

# Tell celery to use RabbitMQ
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ('labmachine.fabsteps.executor',)
CELERYD_CONCURRENCY = 2


FIRST_UWSGI_PORT = 10000
BRANCH_STORE = '/var/www/lieferheld.lab/'
VIRTUALENV_STORE = '/var/www/.virtualenvs/'
LOG_STORE = '/var/www/.branchlogs/'
SUBDOMAIN = 'lieferheld.lab'


FABRIC_HOST = 'www-data@192.168.1.250'
# Environment vars for new branches
ENVIRONMENT_VARS = {'DOWANT_SETTINGS': 'branch_object.settings_file_path',
                    'DJANGO_SETTINGS_MODULE': '\'settings\'',
                    'DOWANT_DB_NAME': 'branch_object.db_name',
                    'DOWANT_BROKER_VHOST': 'branch_object.broker_vhost',
                    'PYTHONHOME': 'branch_object.virtualenv_dir',
                    'PYTHONPATH': '\'%s/:%s/msupport/\' % '\
                        '(branch_object.directory, branch_object.directory)',
                    'PYTHONUNBUFFERED': '\'YEAH\'',
                    'DIR': '\'%s/\'%branch_object.directory',
                    'MAN': '\'%s/dowant/\'%branch_object.code_dir',
                    'DOWANT_BRANCH_URI': '\'http://%s\'%branch_object.uri', }
# Where are the config files templates?
SUPERVISOR_TEMPLATE_PATH='/home/pablo/Escritorio/Workspace/labmachine/fabsteps/services/'
SUPERVISOR_TEMPLATE_LIST = (
    (
        # Path to the template of the celery worker config file
        'celery.conf',
        # Path where the template will be installed
        'config/supervisor/celery.conf',
        # Task name for supervisor group. None if no supervisor
        'celery'),
    # uWSGI
    ('uwsgi.conf',
     'config/supervisor/uwsgi.conf',
     'uwsgi'),
    # Config to group supervisor task
    ('group.conf',
     'config/supervisor/group.conf',
     None),
    # Web server
    ('nginx.conf',
     'config/nginx/lab.conf',
     None),
    )

# Config of celery broker
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_VHOST = 'headquarters'
BROKER_USER = 'headquarters_user'
BROKER_PASSWORD = 'headquarters_user_password'
