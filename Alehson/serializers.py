from rest_framework import serializers
from .models import News, Category, SubCategory, Images, Application
import re
from datetime import date


class BirthDateValidator:
    """Tug‘ilgan sana validatori"""
    def __call__(self, value):
        today = date.today()
        if value >= today:
            raise serializers.ValidationError("Tug‘ilgan sana kelajak sanasi bo‘lishi mumkin emas.")


class PlasticCardValidator:
    """Plastik karta raqamining validatori"""
    def __call__(self, value):
        if not re.match(r"^\d{16}$", value):
            raise serializers.ValidationError("Plastik karta raqamini 16 xonali son sifatida kiriting.")


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'region', 'image', 'created_date', 'view_count', 'slug']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


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
