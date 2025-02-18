from django.db import models

# Create your models here.



class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to="News")
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Images(models.Model):
    image = models.ImageField()


class Application(models.Model):
    full_last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    passport = models.CharField(max_length=20)  
    region = models.CharField(max_length=50)
    birth_date = models.DateField()
    # catigorys = models.ForeignKey("Catigory",on_delete=models.CASCADE)
    descriptions = models.TextField()
    # card_number = models.IntegerField(max_length=20)
    img = models.ManyToManyField(Images)
    
