from io import BytesIO
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

    image_full = models.ImageField(upload_to='media/images')
    image_thumbnail = models.ImageField(upload_to='media/thumbnail', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        image = Image.open(self.image_full).convert('RGB')
        image.thumbnail((200, 200))
        buffer = BytesIO()
        image.save(buffer, format='png')
        val = buffer.getvalue()
        self.image_thumbnail.save(self.image_full.name, ContentFile(val), save=False)
        super().save(*args, **kwargs)
