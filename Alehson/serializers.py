from rest_framework import serializers
from .models import News,Category, SubCategory,Images,Application,Eskizsms
from rest_framework import serializers
import re
from datetime import date




class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','content','region','image','created_date','view_count','slug']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Subkategoriya ma'lumotlarini chiqarish

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']



# class ImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Images
#         fields = ['id', 'image','application']

# class ApplicationSerializer(serializers.ModelSerializer):
#     images = ImagesSerializer(many=True, read_only=True)

#     class Meta:
#         model = Application
#         fields = ['id', 'full_last_name', 'phone', 'passport', 'region', 'birth_date', 'descriptions', 'card_number', 'images']




# class PetitionImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Images
#         fields = ["id", "petition", "image"]


# class EskizSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Eskizsms
#         fields = ('phone_number',)





class PhoneNumberValidator:
    """Telefon raqam validatori"""
    def __call__(self, value):
        if not re.match(r"^\+998\d{9}$", value):
            raise serializers.ValidationError("Telefon raqamini '+998XXXXXXXXX' formatida kiriting.")


class BirthDateValidator:
    """Tug‘ilgan sana validatori"""
    def __call__(self, value):
        today = date.today()
        if value >= today:
            raise serializers.ValidationError("Tug‘ilgan sana kelajak sanasi bo‘lishi mumkin emas.")


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image', 'application']


class ApplicationSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    phone_number = serializers.CharField(validators=[PhoneNumberValidator()])
    birthday = serializers.DateField(validators=[BirthDateValidator()])

    class Meta:
        model = Application
        fields = ['petition_id', "images",'phone_number','birthday','full_name', 'information', 'plastic_card', 'region', 'code', 'category','image','view_count']




class EskizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eskizsms
        fields = ('phone_number',)
