from rest_framework import serializers
from .models import News,Category, SubCategory,Images,Application





class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','content','region','image','created_date','slug']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Subkategoriya ma'lumotlarini chiqarish

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image','application']

class ApplicationSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'full_last_name', 'phone', 'passport', 'region', 'birth_date', 'descriptions', 'card_number', 'images']
