from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.doc_collections.models import DocumentModel, Collection

User = get_user_model()


class WordTfIdfSerializer(serializers.Serializer):
    word = serializers.CharField()
    tf = serializers.FloatField()
    idf = serializers.FloatField()


class DocumentSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner',
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = DocumentModel
        fields = ['title', 'file', 'owner_id']


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentModel
        fields = ['id', 'title']


class DocumentStatisticSerializer(serializers.ModelSerializer):
    collection_id = serializers.IntegerField()
    collection_name = serializers.CharField()
    statistics = WordTfIdfSerializer(many=True)

    class Meta:
        model = DocumentModel
        fields = ['id', 'title', 'collection_id', 'collection_name', 'statistics']


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    documents = DocumentListSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'documents']


class CollectionDetailSerializer(serializers.ModelSerializer):
    documents = DocumentListSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'documents']


class StatisticSerializer(serializers.Serializer):

    statistics = WordTfIdfSerializer(many=True)
