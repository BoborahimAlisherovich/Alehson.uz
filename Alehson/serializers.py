from rest_framework import serializers

from .models import News, Category, SubCategory, Images, Application,Home,About,SiteHelp, Contact,Help,petitionsubmit,AplecationSetings,CategorySettings,ImagesHome,ContactSettings
import re
from datetime import date,datetime
import base64
import requests
import imghdr
from django.core.files.base import ContentFile
from django.utils.text import slugify
from io import BytesIO
from PIL import Image



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


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'content', 'region', 'image', 'view_count', 'created_date', 'slug']
    
    def validate_image(self, value):
        """
        Rasm faqat URL yoki Base64 formatda bo‘lishi mumkin.
        """
        if value and not (value.startswith('http') or value.startswith('data:image')):
            raise serializers.ValidationError("Rasm faqat URL yoki Base64 formatda bo‘lishi mumkin.")
        return value
    
    def validate_title(self, value):
        """
        Agar ushbu sarlavha bilan yangilik allaqachon mavjud bo‘lsa, xatolik qaytaradi.
        """
        if News.objects.filter(title=value).exists():
            raise serializers.ValidationError("Bu sarlavha bilan yangilik allaqachon mavjud.")
        return value
    
    def create(self, validated_data):
        """
        Yangilikni yaratish va rasmni qayta ishlash.
        """
        image_data = validated_data.pop('image', None)
        validated_data['slug'] = self.generate_unique_slug(validated_data['title'])

        if News.objects.filter(slug=validated_data['slug']).exists():
            raise serializers.ValidationError({"slug": "Bu sarlavha bilan yangilik allaqachon mavjud."})
        
        news = News.objects.create(**validated_data)
        
        if image_data:
            success = self.process_image(news, image_data)
            if not success:
                news.delete()
                raise serializers.ValidationError({"image": "Rasmni yuklab bo‘lmadi yoki noto‘g‘ri formatda."})
        
        return news
    
    def generate_unique_slug(self, title):
        """
        Unikal slug yaratadi.
        """
        base_slug = slugify(title)
        slug = base_slug
        count = 1
        while News.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        return slug
    
    def process_image(self, news, image_data):
        """
        URL yoki Base64 orqali yuklangan rasmni qayta ishlash va `.jpg` formatga o‘tkazish.
        """
        if image_data.startswith('http'):
            return self.download_image(news, image_data)
        elif image_data.startswith('data:image'):
            return self.decode_base64_image(news, image_data)
        return False
    
    def convert_to_jpg(self, image_bytes):
        """
        Har qanday turdagi rasmni `.jpg` formatga o‘tkazish.
        """
        image = Image.open(BytesIO(image_bytes))
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        output = BytesIO()
        image.save(output, format="JPEG", quality=90)
        return output.getvalue()
    
    def download_image(self, news, image_url):
        """
        URL orqali rasmni yuklab olib `.jpg` formatga o‘tkazish.
        """
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()
            if response.status_code != 200:
                return False
            file_extension = imghdr.what(None, h=response.content) or "jpg"
            image_bytes = self.convert_to_jpg(response.content)
            file_name = f"news_{news.id}.jpg"
            news.image.save(file_name, ContentFile(image_bytes), save=True)
            return True
        except requests.exceptions.RequestException:
            return False
    
    def decode_base64_image(self, news, base64_string):
        """
        Base64 rasmni dekodlash va `.jpg` formatga o‘tkazish.
        """
        try:
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]
            if ext not in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp']:
                return False
            decoded_file = base64.b64decode(imgstr)
            image_bytes = self.convert_to_jpg(decoded_file)
            file_name = f"news_{news.id}.jpg"
            news.image.save(file_name, ContentFile(image_bytes), save=True)
            return True
        except Exception:
            return False

class SubCategorySerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False, allow_blank=True)  # URL yoki Base64 formatda yuklash uchun
    image_file = serializers.ImageField(required=False)  # Media form orqali yuklash uchun

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'image_file', 'category']

    def validate_image(self, value):
        """
        Rasm URL yoki Base64 bo‘lishi mumkin.
        """
        if value and not (value.startswith('http') or value.startswith('data:image')):
            raise serializers.ValidationError("Rasm faqat URL yoki Base64 formatda bo‘lishi mumkin.")
        return value

    def create(self, validated_data):
        """
        SubCategory yaratish va rasmni qayta ishlash.
        """
        image_data = validated_data.pop('image', None)  # URL yoki Base64
        image_file = validated_data.pop('image_file', None)  # Media form orqali yuklangan rasm

        subcategory = SubCategory(**validated_data)  # Hozircha saqlamaymiz

        try:
            if image_file:
                subcategory.image = image_file  # Media form orqali yuklangan rasm
            elif image_data:
                self.process_image(subcategory, image_data)  # URL yoki Base64 rasmni qayta ishlaymiz

            subcategory.save()  # Hammasi muvaffaqiyatli bo‘lsa, shu yerda saqlaymiz
            return subcategory

        except serializers.ValidationError as e:
            raise e  # Xatolik bo‘lsa, modelni saqlamaymiz

    def update(self, instance, validated_data):
        """
        SubCategory yangilash va rasmni qayta ishlash.
        """
        image_data = validated_data.pop('image', None)
        image_file = validated_data.pop('image_file', None)

        try:
            # Ma'lumotlarni yangilaymiz
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if image_file:
                instance.image = image_file
            elif image_data:
                self.process_image(instance, image_data)  # Yangi rasm yuklash

            instance.save()  # Hammasi muvaffaqiyatli bo‘lsa, shu yerda saqlaymiz
            return instance

        except serializers.ValidationError as e:
            raise e  # Xatolik bo‘lsa, modelni saqlamaymiz

    def process_image(self, subcategory, image_data):
        """
        URL yoki Base64 orqali yuklangan rasmni qayta ishlash va `.jpg` formatga o‘tkazish.
        """
        if image_data.startswith('http'):
            self.download_image(subcategory, image_data)
        elif image_data.startswith('data:image'):
            self.decode_base64_image(subcategory, image_data)

    def convert_to_jpg(self, image_bytes, ext):
        """
        Har qanday turdagi rasmni `.jpg` formatga o‘tkazish.
        """
        image = Image.open(BytesIO(image_bytes))

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        output = BytesIO()
        image.save(output, format="JPEG", quality=90)
        return output.getvalue()

    def download_image(self, subcategory, image_url):
        """
        URL orqali rasmni yuklab olib `.jpg` formatga o‘tkazish.
        """
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()
            file_extension = imghdr.what(None, h=response.content) or "jpg"

            image_bytes = self.convert_to_jpg(response.content, file_extension)
            file_name = f"subcategory_{subcategory.id}.jpg"

            subcategory.image.save(file_name, ContentFile(image_bytes), save=True)
        except requests.exceptions.RequestException:
            raise serializers.ValidationError({"image": "Rasm URL yuklab olinmadi."})

    def decode_base64_image(self, subcategory, base64_string):
        """
        Base64 rasmni dekodlash va `.jpg` formatga o‘tkazish.
        """
        try:
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]

            if ext not in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp']:
                raise serializers.ValidationError({"image": "Yaroqsiz rasm formati."})

            decoded_file = base64.b64decode(imgstr)

            image_bytes = self.convert_to_jpg(decoded_file, ext)
            file_name = f"subcategory_{subcategory.id}.jpg"

            subcategory.image.save(file_name, ContentFile(image_bytes), save=True)
        except Exception:
            raise serializers.ValidationError({"image": "Base64 formatda xatolik bor."})

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']

    def process_image(self, news, image_data):
        """
        URL yoki Base64 orqali yuklangan rasmni qayta ishlash va `.jpg` formatga o‘tkazish.
        """
        if image_data.startswith('http'):
            self.download_image(news, image_data)
        elif image_data.startswith('data:image'):
            self.decode_base64_image(news, image_data)

    def convert_to_jpg(self, image_bytes, ext):
        """
        Har qanday turdagi rasmni `.jpg` formatga o‘tkazish.
        """
        image = Image.open(BytesIO(image_bytes))

        # Agar rasm RGBA bo‘lsa, fonni oq rangga o‘zgartirish
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Rasmni `.jpg` formatiga o‘tkazish
        output = BytesIO()
        image.save(output, format="JPEG", quality=90)
        return output.getvalue()

    def download_image(self, news, image_url):
        """
        URL orqali rasmni yuklab olib `.jpg` formatga o‘tkazish.
        """
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()
            file_extension = imghdr.what(None, h=response.content) or "jpg"

            # Rasmni `.jpg` formatga o‘tkazish
            image_bytes = self.convert_to_jpg(response.content, file_extension)
            file_name = f"news_{news.id}.jpg"

            news.image.save(file_name, ContentFile(image_bytes), save=True)
        except requests.exceptions.RequestException:
            raise serializers.ValidationError({"image": "Rasm URL yuklab olinmadi."})

    def decode_base64_image(self, news, base64_string):
        """
        Base64 rasmni dekodlash va `.jpg` formatga o‘tkazish.
        """
        try:
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]

            if ext not in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp']:
                raise serializers.ValidationError({"image": "Yaroqsiz rasm   formati."})

            decoded_file = base64.b64decode(imgstr)

            # Rasmni `.jpg` formatga o‘tkazish
            image_bytes = self.convert_to_jpg(decoded_file, ext)
            file_name = f"news_{news.id}.jpg"

            news.image.save(file_name, ContentFile(image_bytes), save=True)
        except Exception:
            raise serializers.ValidationError({"image": "Base64 formatda xatolik bor."})

        

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
from rest_framework.serializers import SkipField



class ApplicationSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[BirthDateValidator()])
    plastic_card = serializers.CharField(validators=[PlasticCardValidator()])

    image_urls = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    images = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    # category = CategorySerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday', "is_top",
            'information', 'plastic_card', 'region', 'category','subCategory',  
            'view_count', 'passport_number', 'created_date', 'image_urls', 'images'
        ]

    def get_view_count(self, obj):
        """View count qiymatini qaytarish"""
        return obj.view_count
    
    def get_images(self, obj):
        """Arizaga tegishli rasmlarni to'liq URL shaklida ro‘yxat qilib chiqaradi"""
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]

    def create(self, validated_data):
        """Yangi ariza yaratish va unga tegishli rasmlar URL-larini saqlash"""
        image_urls = validated_data.pop('image_urls', []) 
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


    def to_representation(self, instance):
        # faqat is_active=True bo'lgan obyektlarni qaytarish
        representation = super().to_representation(instance)
        if not instance.is_active:
            pass
        return representation


class ApplicationIsActiveSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[BirthDateValidator()])
    plastic_card = serializers.CharField(validators=[PlasticCardValidator()])
    images = serializers.SerializerMethodField()
    image_urls = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    view_count = serializers.SerializerMethodField()


    class Meta:
        model = Application
        fields = [
            'petition_id', 'full_name', 'phone_number', 'birthday', 'is_top',
            'information', 'plastic_card', 'region', 'category','subCategory',
            'view_count', 'passport_number', 'is_active', 'created_date', 'images','image_urls'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
    
    def get_view_count(self, obj):
        """View count qiymatini qaytarish"""
        return obj.view_count
    
class ImagesHomeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagesHome
        fields = ['id', 'image_url']

    def get_image_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.image.url)

class HomeSeralizer(serializers.ModelSerializer):
    image_urls = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    images = serializers.SerializerMethodField()

    class Meta:
        model = Home
        fields = ["title",'image', "titleAbaut", "description", "image_urls", "images"]

    def get_images(self, obj):
        """Uyga tegishli rasmlarni to'liq URL shaklida ro‘yxat qilib chiqaradi"""
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]

    def create(self, validated_data):
        """Yangi uy yaratish va unga tegishli rasmlar URL-larini saqlash"""
        image_urls = validated_data.pop('image_urls', [])
        home = Home.objects.create(**validated_data)

        for url in image_urls:
            ImagesHome.objects.create(home=home, image=url)  # URL dan rasm saqlash

        return home

class AboutSeralizer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"
    
class SiteHelpSeralizer(serializers.ModelSerializer):
    class Meta:
        model = SiteHelp
        fields = ["title","description","image"]
  
  
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class petitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = petitionsubmit
        fields = '__all__'

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'

class CategorySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySettings
        fields = '__all__'


        
class AplecationSetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplecationSetings
        fields = '__all__'
        

class ContactSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSettings
        fields = '__all__'