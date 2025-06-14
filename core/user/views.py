from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from dj_rest_auth.views import LogoutView

from docs.schemas import user_delete_schema

User = get_user_model()


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @user_delete_schema
    def delete(self, request, pk=None, *args, **kwargs):
        user_id = pk

        if user_id:
            if not request.user.is_staff:
                return Response(
                    {'detail': 'Only admin can delete other users'},
                    status=status.HTTP_403_FORBIDDEN
                )

            user_for_delete = get_object_or_404(User, pk=user_id)

            if user_for_delete.is_staff or user_for_delete.is_superuser:
                return Response(
                    {'detail': 'Can not delete admin users'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_for_delete.delete()

            return Response(
                {"detail": f"User {user_for_delete.username} deleted"},
                status=status.HTTP_204_NO_CONTENT
            )

        user = request.user

        logout_view = LogoutView()
        response = logout_view.post(request)

        # Удаление пользователя
        user.delete()

        return Response(
            {'detail': 'User has been deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
