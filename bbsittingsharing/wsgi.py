"""
WSGI config for bbsittingsharing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys, site
sys.path.insert(0, '/usr/local/alwaysdata/python/django/1.6.4/')
sys.path.insert(0, '/home/bbsittingsharing/bbsittingsharing')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbsittingsharing.settings")
site.addsitedir("/home/bbsittingsharing/.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
