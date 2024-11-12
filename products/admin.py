from django.contrib import admin

from products.models import Product


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
