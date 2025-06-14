from django.urls import path
from core.user import views

urlpatterns = [
    path("delete/", views.UserDeleteView.as_view(), name='user_delete'),
    path("delete/<int:pk>/", views.UserDeleteView.as_view(), name='user_admin_delete'),
]
