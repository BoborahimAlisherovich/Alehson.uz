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

    def __str__(self):
        return f"{self.category.name} → {self.name}"




class News(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
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
    Passport_number = models.CharField(max_length=10)
    region = models.CharField(max_length=300)
    birthday = models.DateField()
    category = models.ForeignKey(Category, related_name='Applications', on_delete=models.CASCADE)
    information = models.TextField()
    plastic_card = models.CharField(max_length=16)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    is_active = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name
    
def user_directory_path(instance, filename): 
    return 'images/{0}/{1}'.format(instance.application.petition_id, filename) 



class Images(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_directory_path, default="", null=True, blank=True)

    def __str__(self):
        return str(self.application)