from typing import Optional

from drf_spectacular.utils import extend_schema, inline_serializer


def create_dict_schema(status: int, name: str, fields: dict, request: Optional = None) -> extend_schema:
    return extend_schema(request=request,
                         responses={status: inline_serializer(
                             name=name,
                             fields=fields
                         )}
                         )
