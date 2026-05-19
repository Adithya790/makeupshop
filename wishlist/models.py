from django.db import models
from products.models import Product


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product',)

    def __str__(self):
        return self.product.name