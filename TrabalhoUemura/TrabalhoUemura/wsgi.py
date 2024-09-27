"""
WSGI config for TrabalhoUemura project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# ANOTAÇÕES - Guilherme
# Interface simples e universal para troca de informações entre servidores web e
# aplicações

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrabalhoUemura.settings')

application = get_wsgi_application()
