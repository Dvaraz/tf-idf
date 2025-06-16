from django.core.files.uploadedfile import UploadedFile

from core.doc_collections.serializers import DocumentSerializer


class DocumentModelAdapter:
    @staticmethod
    def create_document(
            file: UploadedFile,
            title: str = None,
            owner_id: int = None
    ):

        data = {
            'file': file,
            'title': title,
            'owner_id': owner_id
        }

        serializer = DocumentSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
