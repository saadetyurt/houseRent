from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin

from house.models import Category, House, Images

class HouseImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class HouseAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'price', 'room', 'floor', 'm2', 'address', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [HouseImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'house', 'image', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Images, ImagesAdmin)