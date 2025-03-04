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





import requests
import base64
from django.core.files.base import ContentFile
from django.utils.text import slugify
from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False, allow_blank=True)  # URL, Base64 yoki fayl yuklashga ruxsat beradi

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'content', 'region', 'image', 'created_date', 'view_count', 'slug']

    def validate_title(self, value):
        """
        Title asosida slug yaratadi va uning unikalligini tekshiradi.
        """
        new_slug = slugify(value)
        if News.objects.filter(slug=new_slug).exists():
            raise serializers.ValidationError(f"'{new_slug}' slug allaqachon mavjud. Iltimos, boshqa nom tanlang.")
        return value

    def validate_image(self, value):
        """
        Image maydoni URL, Base64 yoki bo‘sh bo‘lishi mumkin.
        """
        if value and not (value.startswith('http') or value.startswith('data:image')):
            raise serializers.ValidationError("Rasm faqat URL yoki Base64 formatda bo‘lishi mumkin.")
        return value

    def create(self, validated_data):
        """
        Yangilikni yaratish va image maydonini qayta ishlash.
        """
        image_data = validated_data.pop('image', None)  # URL yoki Base64 rasmni ajratib olamiz
        validated_data['slug'] = slugify(validated_data['title'])  # Slug yaratamiz

        # Slug unikalligini tekshiramiz
        if News.objects.filter(slug=validated_data['slug']).exists():
            raise serializers.ValidationError({'slug': f"'{validated_data['slug']}' slug allaqachon mavjud. Iltimos, boshqa nom tanlang."})

        # Yangilikni yaratamiz
        news = News.objects.create(**validated_data)

        if image_data:
            if image_data.startswith('http'):  # URL orqali yuklash
                try:
                    response = requests.get(image_data, timeout=5)
                    response.raise_for_status()
                    file_name = image_data.split("/")[-1]
                    news.image.save(file_name, ContentFile(response.content), save=True)
                except requests.exceptions.RequestException:
                    raise serializers.ValidationError({"image": "Rasm URL yuklab olinmadi."})

            elif image_data.startswith('data:image'):  # Base64 orqali yuklash
                try:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    file_name = f"news_{news.id}.{ext}"
                    news.image.save(file_name, ContentFile(base64.b64decode(imgstr)), save=True)
                except Exception:
                    raise serializers.ValidationError({"image": "Base64 formatda xatolik bor."})

        return news


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name','category']

        def validate(self, data):
            if SubCategory.objects.filter(category=data['category'], name=data['name']).exists():
                raise serializers.ValidationError({"name": "Bu nom ushbu kategoriya ichida allaqachon mavjud!"})
            return data

        
import base64
import requests
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Category, SubCategory

class Base64ImageField(serializers.ImageField):
    """URL, Base64 yoki oddiy fayl orqali rasm yuklash imkonini beradi."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith(('http://', 'https://')):
            try:
                response = requests.get(data, timeout=5)
                response.raise_for_status()
                file_name = data.split("/")[-1]  # URLdan fayl nomini olish
                data = ContentFile(response.content, name=file_name)
            except requests.RequestException as e:
                raise serializers.ValidationError(f"URL orqali rasm yuklab bo‘lmadi: {e}")

        elif isinstance(data, str) and data.startswith('data:image'):
            try:
                format, imgstr = data.split(';base64,')  
                ext = format.split('/')[-1]  
                data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
            except Exception:
                raise serializers.ValidationError("Base64 format noto‘g‘ri!")

        return super().to_internal_value(data)

class CategorySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)  # URL, Base64 yoki oddiy fayl yuklashni qo‘llaydi
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # ✅ Kiritish shart emas

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
    created_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday',
            'information', 'plastic_card', 'region', 'category',
            'view_count', 'passport_number', 'image_urls', 'images','created_date'
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
    def get_created_date(self, obj):
        return obj.created_date.strftime('%Y-%m-%d %H:%M:%S')  # Sanani formatlash




class ApplicationIsActiveSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[BirthDateValidator()])
    plastic_card = serializers.CharField(validators=[PlasticCardValidator()])
    images = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday',
            'information', 'plastic_card', 'region', 'category',
            'view_count', 'passport_number', 'is_active', 'images','created_date'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
    def get_created_date(self, obj):
        return obj.created_date.strftime('%Y-%m-%d %H:%M:%S')  # Sanani formatlash
