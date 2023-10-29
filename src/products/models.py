import io
from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.core.files.base import ContentFile
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL
    )

    image_full = models.ImageField(upload_to='images')
    image_thumbnail = models.ImageField(upload_to='thumbnail', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        image = Image.open(self.image_full).convert('RGB')
        image.thumbnail((200, 200))
        buffer = io.BytesIO()
        image.save(buffer, format='png')
        val = buffer.getvalue()
        self.image_thumbnail.save(self.image_full.name, ContentFile(val), save=False)
        super().save(*args, **kwargs)


class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    payment = models.DateTimeField(blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.payment = self.payment + timedelta(days=5)
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
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.pk)
