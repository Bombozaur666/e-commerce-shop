from rest_framework.serializers import ModelSerializer
from .models import Product, WishList
from categories.serializers import CategorySerializer


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "pk",
            "name",
            "description",
            "price",
            "category",
            "image_full",
            "image_thumbnail",
        ]


class WishListSerializer(ModelSerializer):
    product = ProductSerializer

    class Meta:
        model = WishList
        fields = ["product"]
