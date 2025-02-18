from django.contrib import admin

# Register your models here.

from .models import News, Category, SubCategory,Images,Application

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display = ("title", "region", "created_date",)
  prepopulated_fields = {"slug": ("title",)}




class SubCategoryInline(admin.TabularInline):  # Inline ko'rinishda chiqarish
    model = SubCategory
    extra = 1  # Kamida 1 ta bo‘sh input chiqadi

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Admin panelda ko‘rinadigan ustunlar
    inlines = [SubCategoryInline]  # Kategoriyaga tegishli subkategoriyalarni qo‘shish
    



# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category')  # Admin panelda subkategoriya nomi va bog‘langan kategoriyani ko‘rsatish
#     list_filter = ('category',)  # Filtrlash imkoniyati



# class ImageInline(admin.TabularInline):  # Inline ko'rinishda chiqarish
#     model = Images
#     extra = 1  # Kamida 1 ta bo‘sh input chiqadi


# @admin.register(Images)
# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ('image',)


# class ImageInline(admin.TabularInline):
#     model = Application.images.through  # ManyToMany uchun qo‘shish
#     extra = 1



class ImageInline(admin.TabularInline):  # Inline ko'rinishda chiqarish
    model = Images
    extra = 1  # Kamida 1 ta bo‘sh input chiqadi


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_last_name', 'phone', 'passport', 'region', 'birth_date')
    inlines = [ImageInline]

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
