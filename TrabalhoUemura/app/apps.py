from django.apps import AppConfig

# ANOTAÇÕES - Guilherme
# Arquivo responsável pela configuração da app do projeto Django.

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
