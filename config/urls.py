"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from Alehson.views import (
    NewsViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    ApplicationViewSet,
    ImagesViewSet,

    
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
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),


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

    # Subimage CRUD
    path("subimage/", ImagesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("subimage/<int:pk>/", ImagesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),


    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# MEDIA fayllarni xizmat qilish (DEBUG=True bo‘lsa)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

