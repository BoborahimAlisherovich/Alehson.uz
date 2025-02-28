from rest_framework import serializers
from .models import News, Category, SubCategory, Images, Application
import re
from datetime import date,datetime


class BirthDateValidator:
    """Tug‘ilgan sana validatori"""
    
    def __call__(self, value):
        today = date.today()

        # Sana formatini tekshirish
        try:
            datetime.strptime(str(value), "%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError("Tug‘ilgan sana 'YYYY-MM-DD' formatida bo‘lishi kerak.")

        # Kelajak sanani tekshirish
        if value >= today:
            raise serializers.ValidationError("Tug‘ilgan sana kelajak sanasi bo‘lishi mumkin emas.")


class PlasticCardValidator:
    """Plastik karta raqamining validatori"""
    def __call__(self, value):
        if not re.match(r"^\d{16}$", value):
            raise serializers.ValidationError("Plastik karta raqamini 16 xonali son sifatida kiriting.")

import requests
from django.core.files.base import ContentFile

import base64
import requests
from django.core.files.base import ContentFile
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False)  # URL yoki Base64 rasm qabul qilish

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'content', 'region', 'image', 'created_date', 'view_count', 'slug']

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        news = News.objects.create(**validated_data)

        if image_data:
            if image_data.startswith('http'):  # Agar URL bo'lsa, yuklab olish
                response = requests.get(image_data)
                if response.status_code == 200:
                    file_name = image_data.split("/")[-1]
                    news.image.save(file_name, ContentFile(response.content), save=True)
            
            elif image_data.startswith('data:image'):  # Agar Base64 bo‘lsa, saqlash
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"news_{news.id}.{ext}"
                news.image.save(file_name, ContentFile(base64.b64decode(imgstr)), save=True)

        return news


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name','category']

        def validate(self, data):
            if SubCategory.objects.filter(category=data['category'], name=data['name']).exists():
                raise serializers.ValidationError({"name": "Bu nom ushbu kategoriya ichida allaqachon mavjud!"})
            return data

        


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']

from rest_framework import serializers
from .models import Application, Images

class ImagesSerializer(serializers.ModelSerializer):
    """Ariza bilan bog‘liq rasmlar"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = ['id', 'image_url']

    def get_image_url(self, instance):
        """Rasmning to‘liq URL manzilini qaytaradi"""
        request = self.context.get('request')
        return request.build_absolute_uri(instance.image.url) if instance.image else None


class ApplicationSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[BirthDateValidator()])
    plastic_card = serializers.CharField(validators=[PlasticCardValidator()])

    # Foydalanuvchi POST qilish uchun URL jo‘natishi mumkin
    image_urls = serializers.ListField(
        child=serializers.URLField(), write_only=True, required=False
    )

    # GET qilish uchun rasmlar ro‘yxat shaklida chiqadi
    images = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday',
            'information', 'plastic_card', 'region', 'category',
            'view_count', 'passport_number', 'image_urls', 'images'
        ]

    def get_images(self, obj):
        """Arizaga tegishli rasmlarni to'liq URL shaklida ro‘yxat qilib chiqaradi"""
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]

    def create(self, validated_data):
        """Yangi ariza yaratish va unga tegishli rasmlar URL-larini saqlash"""
        image_urls = validated_data.pop('image_urls', [])  # Foydalanuvchi kiritgan URL larni olish
        application = Application.objects.create(**validated_data)

        for url in image_urls:
            Images.objects.create(application=application, image=url)  # URL dan rasm saqlash

        return application

    def validate(self, data):
        """Telefon raqam va pasport raqami bo‘yicha ariza mavjudligini tekshiradi"""
        phone_number = data.get('phone_number')
        passport_number = data.get('passport_number')  # Katta harf bilan bo'lgan xatolik tuzatildi

        if Application.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "Bu telefon raqami bilan allaqachon ariza yaratilgan!"})

        if Application.objects.filter(passport_number=passport_number).exists():
            raise serializers.ValidationError({"passport_number": "Bu pasport raqami bilan allaqachon ariza yaratilgan!"})

        return data
