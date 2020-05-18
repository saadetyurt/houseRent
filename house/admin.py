from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

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

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_houses_count', 'related_houses_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                House,
                'category',
                'houses_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 House,
                 'category',
                 'houses_count',
                 cumulative=False)
        return qs

    def related_houses_count(self, instance):
        return instance.houses_count
    related_houses_count.short_description = 'Related houses (for this specific category)'

    def related_houses_cumulative_count(self, instance):
        return instance.houses_cumulative_count
    related_houses_cumulative_count.short_description = 'Related houses (in tree)'

admin.site.register(Category, CategoryAdmin2)
admin.site.register(House, HouseAdmin)
admin.site.register(Images, ImagesAdmin)