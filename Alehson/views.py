# from django.shortcuts import render
# from rest_framework import viewsets, permissions,viewsets
# from .models import News, Application,Images, Category, SubCategory
# from .serializers import NewsSerializer,ApplicationSerializer,CategorySerializer, SubCategorySerializer,ImagesSerializer


# # Create your views here.
# # class NewsViewSet(viewsets.ModelViewSet):
# #     serializer_class = NewsSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def get_queryset(self):
# #         return News.objects.all().order_by('-id')
    

# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status

# class NewsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.all().order_by('-id')
#     serializer_class = NewsSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     @action(detail=True, methods=['POST'])
#     def increment_view_count(self, request, pk=None):
#         """Ko‘rishlar sonini oshirish"""
#         news = self.get_object()
#         news.view_count += 1
#         news.save()
#         return Response({'message': 'View count incremented', 'view_count': news.view_count}, status=status.HTTP_200_OK)




# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class SubCategoryViewSet(viewsets.ModelViewSet):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubCategorySerializer

# class ApplicationViewSet(viewsets.ModelViewSet):
#     """Arizalar API - Ko‘rishlar sonini oshirish funksiyasi bilan"""
#     serializer_class = ApplicationSerializer

#     def get_queryset(self):
#         """Faqat admin tasdiqlagan (is_active=True) arizalarni chiqarish"""
#         return Application.objects.filter(is_active=True).order_by('-petition_id')

#     def perform_create(self, serializer):
#         """Yangi ariza yaratilganda is_active maydonini o‘zgartira olmasin"""
#         serializer.save(is_active=False)

#     @action(detail=True, methods=['POST'])
#     def increment_view_count(self, request, pk=None):
#         """Ko‘rishlar sonini oshirish"""
#         application = self.get_object()
#         application.view_count += 1
#         application.save()
#         return Response({'message': 'View count incremented', 'view_count': application.view_count}, status=status.HTTP_200_OK)

# class ImagesViewSet(viewsets.ModelViewSet):
#     queryset = Images.objects.all()
#     serializer_class = ImagesSerializer





from django.shortcuts import render
from rest_framework import viewsets, permissions, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import random
from .models import News, Application, Images, Category, SubCategory, Eskizsms
from .serializers import NewsSerializer, ApplicationSerializer, CategorySerializer, SubCategorySerializer, ImagesSerializer, EskizSerializer
from .utils import SendSmsApiWithEskiz

# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def increment_view_count(self, request, pk=None):
        """Ko‘rishlar sonini oshirish"""
        news = self.get_object()
        news.view_count += 1
        news.save()
        return Response({'message': 'View count incremented', 'view_count': news.view_count}, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    """Arizalar API - Ko‘rishlar sonini oshirish funksiyasi bilan"""
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        """Faqat admin tasdiqlagan (is_active=True) arizalarni chiqarish"""
        return Application.objects.filter(is_active=True).order_by('-petition_id')

    def perform_create(self, serializer):
        """Yangi ariza yaratilganda is_active maydonini o‘zgartira olmasin"""
        serializer.save(is_active=False)

    @action(detail=True, methods=['POST'])
    def increment_view_count(self, request, pk=None):
        """Ko‘rishlar sonini oshirish"""
        application = self.get_object()
        application.view_count += 1
        application.save()
        return Response({'message': 'View count incremented', 'view_count': application.view_count}, status=status.HTTP_200_OK)

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Eskizsms
from .serializers import EskizSerializer
from .utils import SendSmsApiWithEskiz
import random

class CreateEskizview(generics.CreateAPIView):
    queryset = Eskizsms.objects.all()
    serializer_class = EskizSerializer

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']

        # Check if phone number already exists in Eskizsms
        existing_entry = Eskizsms.objects.filter(phone_number=phone_number).first()

        # Generate a random verification code
        random_number = random.randint(10000, 99999)
        message = f"Bu Alehson. Sizning kodingiz: {random_number}"
        phone = phone_number[-9:]

        # Create the Eskiz API object and send the SMS
        eskiz_api = SendSmsApiWithEskiz(message=message, phone=int(phone))

        try:
            # Send SMS via Eskiz API
            r = eskiz_api.send()

            # Check if the response contains the required token
            if r and 'data' in r and 'token' in r['data']:
                token = r['data']['token']
            else:
                raise ValueError("Failed to get token from Eskiz API response.")

        except Exception as e:
            # Handle any errors that occur when sending the SMS
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if existing_entry:
            # If entry exists, update verification code
            existing_entry.verification_code = str(random_number)
            existing_entry.save()

            return Response({'verification_code': existing_entry.verification_code}, status=status.HTTP_200_OK)
        else:
            # Create a new Eskizsms entry with the generated verification code
            serializer.save(verification_code=str(random_number))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
