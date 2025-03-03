from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News, Application, Images, Category, SubCategory
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import pagination


from .serializers import (
    NewsSerializer,
    ApplicationSerializer,
    CategorySerializer,
    SubCategorySerializer,
    ImagesSerializer,
    ApplicationIsActiveSerializer,
)




# Custom Pagination class
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12  # Har bir sahifada 10 ta element bo'ladi
    page_size_query_param = 'page_size'  # Foydalanuvchi query orqali o'zgartirishi mumkin
    max_page_size = 100  # Maksimal sahifa hajmi

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination  # Pagination qo'shildi

    def perform_update(self, serializer):
        instance = self.get_object()
        if 'title' in serializer.validated_data:
            serializer.validated_data['slug'] = slugify(serializer.validated_data['title'])
        serializer.save()

    @action(detail=True, methods=['POST'])
    def increment_view_count(self, request, pk=None):
        news = self.get_object()
        news.view_count += 1
        news.save()
        return Response({'message': 'View count incremented', 'view_count': news.view_count}, status=status.HTTP_200_OK)


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
    queryset = Application.objects.all().order_by('-petition_id')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['POST'])
    def increment_view_count(self, request, pk=None):
        application = self.get_object()
        application.view_count += 1
        application.save()
        return Response({'message': 'View count incremented', 'view_count': application.view_count}, status=status.HTTP_200_OK)



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
