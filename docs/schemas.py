from rest_framework import serializers, status

from docs.schema_factory import create_dict_schema


def upload_response_schema(request):
    return create_dict_schema(
        status=status.HTTP_201_CREATED,
        request=request,
        name="Upload",
        fields={
            "word": serializers.CharField(),
            "tf": serializers.IntegerField(),
            "docs": serializers.DictField(),
            "idf": serializers.FloatField()
        }
    )


status_response_schema = create_dict_schema(
    status=status.HTTP_200_OK,
    name="Status",
    fields={
        "status": serializers.CharField()
    }
)

api_info_response_schema = create_dict_schema(
    status.HTTP_200_OK,
    name="ApiInfo",
    fields={
        "name": serializers.CharField(),
        "version": serializers.IntegerField()
    }
)

metrics_response_schema = create_dict_schema(
    status.HTTP_200_OK,
    name="Metrics",
    fields={
            'files_processed': serializers.IntegerField(),
            'min_time_processed': serializers.FloatField(),
            'avg_time_processed': serializers.FloatField(),
            'max_time_processed': serializers.FloatField(),
            'latest_file_processed_timestamp': serializers.DateTimeField(),
            'success_files': serializers.IntegerField(),
            'peak_memory_usage': serializers.FloatField(),
    }
)
