from django.urls import path
from core.tfidf_app import views

urlpatterns = [
    path("upload/", views.FileUploadView.as_view(), name='upload_document'),
    path("status/", views.StatusGetView.as_view(), name='app_status'),
    path("version/", views.ApiInfo.as_view(), name='app_version'),
    path("metrics/", views.MetricsView.as_view(), name='metrics'),
]
