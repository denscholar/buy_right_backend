from django.contrib import admin

from products.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "product_url",
        "image_url",
        "product_price",
        "created_at",
        "updated_at",
    )
    list_display_links = ("product_name",)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    list_display_links = ("name",)
