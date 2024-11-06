from django.contrib import admin
from .models import Category, Discount

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'category', 'status', 'valid_from', 'valid_until')
    list_filter = ('category', 'status')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
