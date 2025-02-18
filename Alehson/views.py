from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import News
from .serializers import NewsSerializer

# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return News.objects.all()