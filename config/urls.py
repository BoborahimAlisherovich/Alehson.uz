from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from Alehson.views import (
    NewsViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    ApplicationViewSet,
    ApplicationIsActiveViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Alehson API",
        default_version='v1',
        description="API documentation for the Alehson platform.",
        contact=openapi.Contact(email="Alehson77@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # News CRUD
    path("news/", NewsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("news/<int:pk>/", NewsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Categories CRUD
    path("categories/", CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("categories/<int:pk>/", CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Subcategories CRUD
    path("subcategories/", SubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("subcategories/<int:pk>/", SubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Applications CRUD
    path("application/", ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("application/<int:pk>/", ApplicationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path("application/<int:pk>/increment/", ApplicationViewSet.as_view({'post': 'increment_view_count'})),

    # Application Is Active CRUD
    path("application-is-active/", ApplicationIsActiveViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("application-is-active/<int:pk>/", ApplicationIsActiveViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("application-is-active/<int:pk>/toggle/", ApplicationIsActiveViewSet.as_view({'patch': 'toggle_active_status'})),

   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
