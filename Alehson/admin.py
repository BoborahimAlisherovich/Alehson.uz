from django.contrib import admin

# Register your models here.

from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display = ("title", "region", "created_date",)
  prepopulated_fields = {"slug": ("title",)}
