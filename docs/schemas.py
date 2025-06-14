from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import serializers, status

from docs.schema_factory import create_dict_schema, general_response_schema


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


user_delete_schema = general_response_schema(
    summary='Удалить пользователя',
    description="""
            Позволяет:
            1. Текущему пользователю удалить свой аккаунт
            2. Администратору удалить любой аккаунт (при указании user_id)
            
             **Права доступа:**
            - Все аутентифицированные пользователи могут удалить себя
            - Только администраторы могут удалять других пользователей
    
            **Важно:**
            - Все связанные данные будут удалены безвозвратно
            - Требует JWT-аутентификации
            """,
    responses={
        204: OpenApiResponse(
            description="Пользователь удален",
            examples=[
                OpenApiExample(
                    name="Success",
                    value={"detail": "User deleted"},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
                description="Неверный запрос",
                examples=[
                    OpenApiExample(
                        name="Error",
                        value={"error": "Can not delete admin users"},
                        response_only=True
                    )
                ]
            ),
        401: OpenApiResponse(
            description="Не авторизован",
            examples=[
                OpenApiExample(
                    name="Error",
                    value={"detail": "Authentication credentials were not provided."},
                    response_only=True
                )
            ]
        ),
        403: OpenApiResponse(
                description="Неверный запрос",
                examples=[
                    OpenApiExample(
                        name="Error",
                        value={"error": "Only admin can delete other users"},
                        response_only=True
                    )
                ]
            ),
        500: OpenApiResponse(
            description="Ошибка сервера",
            examples=[
                OpenApiExample(
                    name="Error",
                    value={"error": "Internal server error"},
                    response_only=True
                )
            ]
        )

    },
    methods=["DELETE"]
)
