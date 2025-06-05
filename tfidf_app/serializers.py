from rest_framework import serializers
from tfidf_app.models import Metrics


class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.txt'):
            raise serializers.ValidationError('only txt')
        return value


class MetricsInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics
        fields = [
            "file_name",
            "processing_time",
            "status",
            "memory_usage",
        ]

