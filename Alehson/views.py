from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import News, Application,Images
from .serializers import NewsSerializer,ApplicationSerializer

# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return News.objects.all().order_by('-id')
    

from rest_framework import viewsets
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer,ImagesSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

