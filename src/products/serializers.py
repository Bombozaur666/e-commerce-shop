from rest_framework.serializers import ModelSerializer
from .models import Product
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
