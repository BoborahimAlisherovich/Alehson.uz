from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News, Application, Images, Category, SubCategory,Home,About,SiteHelp, Contact, CategorySettings,Help,petitionsubmit,AplecationSetings,ContactSettings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import pagination
from django.utils.text import slugify
from hitcount.views import HitCountMixin

from .serializers import (
    NewsSerializer,
    ApplicationSerializer,
    CategorySerializer,
    SubCategorySerializer,
    ImagesSerializer,
    ApplicationIsActiveSerializer,
    SiteHelpSeralizer,
    AboutSeralizer,
    HomeSeralizer,
    ContactSerializer,
    CategorySettingsSerializer,
    AplecationSetingsSerializer,
    HelpSerializer,
    petitionSerializer,
    ContactSettingsSerializer

    
)




# Custom Pagination class
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12  # Har bir sahifada 10 ta element bo'ladi
    page_size_query_param = 'page_size'  # Foydalanuvchi query orqali o'zgartirishi mumkin
    max_page_size = 100  # Maksimal sahifa hajmi



class NewsViewSet(viewsets.ModelViewSet, HitCountMixin):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination  

    def perform_update(self, serializer):
        instance = self.get_object()
        if 'title' in serializer.validated_data:
            serializer.validated_data['slug'] = slugify(serializer.validated_data['title'])
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1  # Yangi qiymatni tayin qilamiz
        obj.save()
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  



class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)  

    def create(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({"error": "Image file required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.filter(is_active=True).order_by('-petition_id')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
 

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1 
        obj.save()
        return super().retrieve(request, *args, **kwargs)
    


class ApplicationIsActiveViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-petition_id')
    serializer_class = ApplicationIsActiveSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['PATCH'])
    def toggle_active_status(self, request, pk=None):
        application = self.get_object()
        application.is_active = not application.is_active
        application.save()
        return Response({'message': 'Application active status changed', 'is_active': application.is_active}, status=status.HTTP_200_OK)

    


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSeralizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSeralizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SiteHelpViewSet(viewsets.ModelViewSet):
    queryset = SiteHelp.objects.all()
    serializer_class = SiteHelpSeralizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class CategorySettingsViewSet(viewsets.ModelViewSet):
    queryset = CategorySettings.objects.all()
    serializer_class = CategorySettingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AplecationSetingsViewSet(viewsets.ModelViewSet):
    queryset = AplecationSetings.objects.all()
    serializer_class = AplecationSetingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class petitionViewSet(viewsets.ModelViewSet):
    queryset = petitionsubmit.objects.all()
    serializer_class = petitionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContactSettingsViewSet(viewsets.ModelViewSet):
    queryset = ContactSettings.objects.all()
    serializer_class = ContactSettingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]