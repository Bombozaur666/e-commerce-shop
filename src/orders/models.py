from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from products.models import Product


# Create your models here.
class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    created = models.DateField(blank=True)

    date_of_payment = models.DateField(blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.created = datetime.now()
        self.date_of_payment = self.created.date() + timedelta(days=5)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.pk)
