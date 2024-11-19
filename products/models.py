from django.db import models
import uuid
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=350, unique=True, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250, blank=True, null=True)
    product_url = models.URLField(max_length=350, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True) 
    image_url = models.URLField(max_length=350,blank=True, null=True)
    product_price = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=350, unique=True, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name) + str(uuid.uuid4())

        # if self.slug:
        #     original = Product.objects.get(slug=self.slug)
        #     if original.product_price != self.product_price:
        #         # Record the price change in ProductPriceHistory
        #         ProductPriceHistory.objects.create(
        #             product=self,
        #             price=original.product_price
        #         )

        super().save(*args, **kwargs)
    
class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, related_name='price_history', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)