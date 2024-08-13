from django.apps import AppConfig
from django.db import connection


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        with connection.cursor() as cursor:
            cursor.execute("SET TIMEZONE TO 'Asia/Tokyo';")
