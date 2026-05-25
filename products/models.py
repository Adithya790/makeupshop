# products/models.py

from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    # Parent category for subcategories
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):

        if self.parent:
            return f"{self.parent.name} → {self.name}"

        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


# ADD THIS NEW MODEL
class CategoryBanner(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='banners'
    )

    image = models.ImageField(
        upload_to='category_banners/'
    )

    def __str__(self):
        return f"{self.category.name} Banner"


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/')

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
