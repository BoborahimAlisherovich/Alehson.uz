from django.contrib import admin

# Register your models here.

from .models import News, Category, SubCategory,Images,Application,Home,About,SiteHelp, Contact, ImagesHome

# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#   list_display = ("title", "region", "created_date",)
#   prepopulated_fields = {"slug": ("title",)}


from django.contrib import admin
from django.utils.text import slugify
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'created_date', 'view_count')
    readonly_fields = ('slug', 'view_count')  # Admin panelda slug va view_count o‘zgartirib bo‘lmaydi
    fields = ('title', 'description','content', 'region', 'image', 'slug', 'view_count')  # Formaga slugni qo‘shish
    
    def save_model(self, request, obj, form, change):
        if not obj.slug or 'title' in form.changed_data:  # Title o‘zgarganda slug ham yangilansin
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

admin.site.register(News, NewsAdmin)



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



class ImageInline(admin.TabularInline):  # Inline ko'rinishda chiqarish
    model = Images
    extra = 1  # Kamida 1 ta bo‘sh input chiqadi

class HomeImageInline(admin.TabularInline):
    model = ImagesHome
    extra = 1

@admin.register(Application)    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_number', 'birthday', 'is_active')
    inlines = [ImageInline]


# @admin.register(Images)
# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'image')


# @admin.register(Images)
# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'image', 'application')


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [HomeImageInline]

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_thick')

@admin.register(SiteHelp)
class SiteHelpAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'message')

