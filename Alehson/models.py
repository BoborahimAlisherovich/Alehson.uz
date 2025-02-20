from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="Images/categories/", blank=True, null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} → {self.name}"

from ckeditor.fields import RichTextField

class News(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/News")
    created_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'



    

class Application(models.Model):
  
  petition_id = models.AutoField(primary_key=True)
  full_name = models.CharField(max_length=100)
  phone_number = models.CharField(max_length=13)
  birthday = models.DateField()
  information = models.TextField()
  plastic_card = models.CharField(max_length=16)
  is_active = models.BooleanField(default=False)
  view_count = models.IntegerField(default=0)
  image = models.ImageField(upload_to = 'images/',  blank = True, null=True, default='')
  region = models.CharField(max_length=300)
  code = models.CharField(max_length=5)
  category = models.ForeignKey(Category,related_name='Applications',on_delete=models.CASCADE,blank=True, null=True)

  def __str__(self):
        return self.full_name

def user_directory_path(instance, filename): 
  
    return 'images/{0}/{1}'.format(instance.petition.petition_id, filename) 



class Eskizsms(models.Model):
    phone_number = models.CharField(max_length=13)
    verification_code = models.CharField(max_length=5)
    def __str__(self):
        return self.phone_number


class Images(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="Images/Application/")

    def __str__(self):
        return f"{self.application.full_name} → {self.image}"

    

   