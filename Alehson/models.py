from django.db import models
from ckeditor.fields import RichTextField



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="Images/categories/", blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/subcategories/", blank=True, null=True)


    class Meta:
        unique_together = ('category', 'name')  

    def __str__(self):
        return f"{self.category.name} → {self.name}"



from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class News(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    description = models.TextField()

    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/News")
    created_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, editable=False)  # Admin panelda o‘zgartirib bo‘lmaydi

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
        information = models.TextField()
        plastic_card = models.CharField(max_length=16)
        is_active = models.BooleanField(default=False)
        view_count = models.IntegerField(default=0)
        created_date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.full_name
        
    # def user_directory_path(instance, filename): 
    #     return 'images/{0}/{1}'.format(instance.application.petition_id, filename) 



class Images(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/applications/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.application.full_name}"