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


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id','image','application']

class ApplicationSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[BirthDateValidator()])
    plastic_card = serializers.CharField(validators=[PlasticCardValidator()])
    images = ImagesSerializer(many=True, read_only=True)  # `imagess` o‘rniga `images`

    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday',
            'information', 'plastic_card', 'region', 'category',
            'image', 'view_count', 'Passport_number', 'images'  # `imagess` ni `images` ga almashtirish
        ]


    def validate(self, data):
        """Telefon raqam va pasport raqam bo‘yicha ariza mavjudligini tekshiradi"""
        phone_number = data.get('phone_number')
        passport_number = data.get('Passport_number')

        if Application.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "Bu telefon raqami bilan allaqachon ariza yaratilgan!"})

        if Application.objects.filter(Passport_number=passport_number).exists():
            raise serializers.ValidationError({"Passport_number": "Bu pasport raqami bilan allaqachon ariza yaratilgan!"})

        return data
