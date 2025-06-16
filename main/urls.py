from django.contrib import admin
from django.urls import path, include

from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path(
        'api/v1/auth/password/reset/confirm/<int:uidb64>/<str:token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path('api/v1/', include("core.tfidf_app.urls")),
    path('api/v1/docs/', include("core.doc_collections.urls")),
    path('api/v1/user/', include("core.user.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
