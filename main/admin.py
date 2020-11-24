from django.contrib import admin
from main.models import Pet, Category, Product, Help

# Register your models here.
admin.site.register(Pet)
admin.site.register(Category)
admin.site.register(Help)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","category","price"]

    class Meta:
        model=Product
