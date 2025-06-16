from django.db.models.signals import post_delete
from django.dispatch import receiver
from core.doc_collections.models import DocumentModel


@receiver(post_delete, sender=DocumentModel)
def delete_document_file(sender, instance, **kwargs):
    """
    Удаляет файл с диска при удалении объекта DocumentModel
    """
    if instance.file:
        instance.file.delete(save=False)