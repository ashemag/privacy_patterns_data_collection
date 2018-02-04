"""
WSGI config for privacy_patterns_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "privacy_patterns_app.settings")
application = WhiteNoise(application, root='../display_data_app/static/images')
# application.add_files('/path/to/more/static/files', prefix='more-files/')