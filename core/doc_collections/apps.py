from django.apps import AppConfig


class DocCollectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.doc_collections'

    def ready(self):
        from core.doc_collections import signals
