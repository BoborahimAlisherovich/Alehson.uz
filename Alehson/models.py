from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="Images/categories/", blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/subcategories/")


    class Meta:
        unique_together = ('category', 'name')  

    def __str__(self):
        return f"{self.category.name} → {self.name}"




class News(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    description = models.TextField()
    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/News")
    created_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, editable=False)  # Admin panelda o‘zgartirib bo‘lmaydi

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Kirillchani lotinga o‘giradi
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


from django.core.exceptions import ValidationError

# ✅ Slugni avtomatik yaratish va mavjud slug'ni tekshirish
def set_news_slug(sender, instance, **kwargs):
    new_slug = slugify(instance.title)

    # Agar slug allaqachon mavjud bo‘lsa, xatolik qaytarish
    if News.objects.filter(slug=new_slug).exclude(id=instance.id).exists():
        raise ValidationError(f"'{new_slug}' slug allaqachon mavjud. Iltimos, boshqa nom tanlang.")

    instance.slug = new_slug


pre_save.connect(set_news_slug, sender=News)
    

class Application(models.Model):
        petition_id = models.AutoField(primary_key=True)
        full_name = models.CharField(max_length=100)
        phone_number = models.CharField(max_length=13)
        passport_number = models.CharField(max_length=10)
        region = models.CharField(max_length=300)
        birthday = models.DateField()
        category = models.ForeignKey(Category, related_name='Applications', on_delete=models.CASCADE)
        subCategory = models.ForeignKey(SubCategory, related_name='applications', on_delete=models.CASCADE,blank=True, null=True)

        information = models.TextField()
        plastic_card = models.CharField(max_length=16)
        is_active = models.BooleanField(default=False)
        is_top = models.BooleanField(default=False)
        view_count = models.IntegerField(default=0)
        created_date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.full_name
        


class Images(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/applications/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.application.full_name}"
    


#site settings 

class Home(models.Model):
    image = models.ImageField(upload_to="images/home/", blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    titleAbaut = models.CharField(max_length=100,blank=True, null=True) 
    description = models.TextField(blank=True, null=True)

    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if Home.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta Home yozuvi qo‘shish mumkin!")


    def __str__(self):
        return self.title

class ImagesHome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/home/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.home.title}"

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Help(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="Images/Help", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    
    def clean(self):
        """Modeldan faqat 3 ta nusxa bo‘lishini tekshirish"""
        if Help.objects.count() >= 3 and not self.pk:
            raise ValidationError("Faqat 3 ta Help yozuvi qo‘shish mumkin!")
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Validatsiya ishga tushadi
        self.slug = slugify(self.title)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class About(models.Model):
    image_main = models.ImageField(upload_to="Images/About",blank=True, null=True)
    image = models.ImageField(upload_to="Images/About",blank=True, null=True)
    main_title = models.CharField(max_length=100,blank=True, null=True)

    thick_title = models.CharField(max_length=100,blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)

    mission_title = models.CharField(max_length=100,blank=True, null=True)
    mission_description = models.TextField(blank=True, null=True)

    vision_title = models.CharField(max_length=100,blank=True, null=True)
    vision_description = models.TextField(blank=True, null=True)

    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if About.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta About yozuvi qo‘shish mumkin!")



    def __str__(self):
        return self.main_title

class SiteHelp(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="Images/SiteHelp",blank=True, null=True)
    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if SiteHelp.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta SiteHelp yozuvi qo‘shish mumkin!")

    def __str__(self):
        return self.title
    

class AplecationSetings(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    image = models.ImageField(upload_to="Images/AplecationSetings",blank=True, null=True)

    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if AplecationSetings.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta AplecationSetings yozuvi qo‘shish mumkin!")


    def __str__(self):
        return self.title
    
class petitionsubmit(models.Model):
    image = models.ImageField(upload_to="Images/petitionsubmit",blank=True, null=True)
    title = models.CharField(max_length=100,blank=True, null=True)

    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if petitionsubmit.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta petitionsubmit yozuvi qo‘shish mumkin!")

    def __str__(self):
        return self.title


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"        
    

class ContactSettings(models.Model):
    image = models.ImageField(upload_to="Images/ContactSettings",blank=True, null=True)
    title = models.CharField(max_length=100,blank=True, null=True)
    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if ContactSettings.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta ContactSettings yozuvi qo‘shish mumkin!")

    

class CategorySettings(models.Model):
    image = models.ImageField(upload_to="images/categories_settings/", blank=True, null=True, verbose_name="Image")
    title = models.CharField(max_length=255, verbose_name="Title")

    def clean(self):
        """Modeldan faqat bitta nusxa bo‘lishini tekshirish"""
        if CategorySettings.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta CategorySettings yozuvi qo‘shish mumkin!")

    
    def __str__(self):
        return self.title

