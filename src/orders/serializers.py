from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    IntegerField,
)
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from accounts.serializers import UserSerializer


class StatisticSerializer(Serializer):
    product__name = CharField()
    quantity = IntegerField()


class OrderSerializer(ModelSerializer):
    client = UserSerializer()

    class Meta:
        model = Order
        fields = ["client", "address", "city", "postal_code", "created", "date_of_payment"]


class OrderItemSerializer(ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["order", "product", "price", "quantity"]
