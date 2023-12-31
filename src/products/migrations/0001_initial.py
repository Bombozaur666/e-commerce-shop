# Generated by Django 4.2.1 on 2023-11-02 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=2000)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("image_full", models.ImageField(upload_to="images")),
                ("image_thumbnail", models.ImageField(blank=True, upload_to="thumbnail")),
                (
                    "category",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="categories.category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WishList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="wishlist", to="products.product"
                    ),
                ),
            ],
        ),
    ]
