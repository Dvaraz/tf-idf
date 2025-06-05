from django.urls import path
from tfidf_app import views

urlpatterns = [
    path("upload/", views.FileUploadView.as_view()),
    path("status/", views.StatusGetView.as_view()),
    path("version/", views.ApiInfo.as_view()),
    path("metrics/", views.MetricsView.as_view()),
]
