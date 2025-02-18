from django.db import models

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
    content = models.TextField()
    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Images/News")
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'




class Application(models.Model):
    full_last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    passport = models.CharField(max_length=20)  
    region = models.CharField(max_length=50)
    birth_date = models.DateField()
    # catigorys = models.ForeignKey("Catigory",on_delete=models.CASCADE)

    descriptions = models.TextField()
    card_number = models.BigIntegerField()
    # images = models.ManyToManyField(Images, related_name="applications")

    def __str__(self):
        return self.full_last_name



# class Images(models.Model):
#     image = models.ImageField(upload_to="Images/Application/")
#     application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="Applications_images")


#     def __str__(self):
#         return f"{self.application.full_last_name}→ {self.image}"
    

class Images(models.Model):
    image = models.ImageField(upload_to="Images/Application/")
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="images")  # related_name yangilandi

    def __str__(self):
        return f"{self.application.full_last_name}→ {self.image}"

    

   
    



    # def __str__(self):
    #     return f"Image {self.id}"

