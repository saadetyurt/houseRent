from django.contrib import admin

# Register your models here.
from house.models import Category, House


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
class HouseAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'price', 'room', 'floor', 'm2', 'image', 'status']
    list_filter = ['status', 'category']
admin.site.register(Category, CategoryAdmin)
admin.site.register(House, HouseAdmin)