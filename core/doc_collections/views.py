import string
from itertools import chain

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.doc_collections.models import DocumentModel, Collection
from core.doc_collections.serializers import DocumentListSerializer, CollectionSerializer, CollectionCreateSerializer, \
    CollectionDetailSerializer, DocumentStatisticSerializer, StatisticSerializer
from core.tfidf_app.utils import preprocess_text, compute_tf, clean_text, compute_tf_idf_for_document


class DocumentsListView(ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DocumentModel.objects.filter(owner=self.request.user)


class DocumentContentView(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DocumentModel.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def get_content(self, request, pk=None, *args, **kwargs):

        document = get_object_or_404(DocumentModel, pk=pk, owner=request.user)
        try:
            with open(document.file.path, 'r') as file:
                content = file.read().replace('\n', '')
            return Response({'content': content})
        except IOError:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DocumentStatisticView(RetrieveModelMixin, GenericViewSet):

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        document_for_stat = get_object_or_404(DocumentModel, pk=pk, owner=request.user)
        collections = document_for_stat.collections.all()

        if not collections:
            return Response(
                {"error": "Document is not presented in any collection"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with open(document_for_stat.file.path, 'r') as file:
                content = file.read()
        except IOError:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        doc = clean_text(content).split()

        collections_stats = []
        for collection in collections:
            collection_documents = []

            for document in collection.documents.all():
                try:
                    with open(document.file.path, 'r') as file:
                        doc_content = file.read()
                        doc_content = clean_text(doc_content).split()
                        collection_documents.append(doc_content)
                except IOError:
                    continue

            stats = compute_tf_idf_for_document(doc, collection_documents)

            collections_stats.append({
                'id': document_for_stat.id,
                'title': document_for_stat.title,
                'collection_id': collection.id,
                'collection_name': collection.name,
                'statistics': stats
            })

        serializer = DocumentStatisticSerializer(
            collections_stats,
            many=True
        )

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class CollectionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionCreateSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class CollectionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionDetailSerializer

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class CollectionListView(ListAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class CollectionModifyView(RetrieveModelMixin, GenericViewSet):
    serializer_class = CollectionDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def modify_collection(self, request, pk=None, document_id=None, *args, **kwargs):

        collection = get_object_or_404(Collection, pk=pk, owner=request.user)
        document = get_object_or_404(DocumentModel, id=document_id, owner=request.user)

        if request.method == 'POST':
            if collection.documents.filter(id=document.id).exists():
                return Response(
                    {'error': 'Document already in collection'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            collection.documents.add(document)
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'DELETE':
            if not collection.documents.filter(id=document.id).exists():
                return Response(
                    {'error': 'Document not in collection'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            collection.documents.remove(document)
            return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionStatisticView(RetrieveModelMixin, GenericViewSet):

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        collection = get_object_or_404(Collection, pk=pk, owner=request.user)

        documents = collection.documents.all()

        if not documents:
            if not documents:
                return Response(
                    {"error": "Collection has no documents"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        texts = []

        for document in documents:
            try:
                with open(document.file.path, 'r') as file:
                    text = file.read()
                    text = clean_text(text)
                    texts.append(text)
            except IOError:
                continue

        all_text = ''.join(texts).split()
        texts = [text.split() for text in texts]

        result = compute_tf_idf_for_document(all_text, texts)

        data = StatisticSerializer({'statistics': result})

        return Response({'data': data.data}, status.HTTP_200_OK)
