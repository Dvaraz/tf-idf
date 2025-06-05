from django.contrib import admin
from django.urls import path, include
from tfidf_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.upload_file, name='upload')
    path("api/", include("tfidf_app.urls"))
]
