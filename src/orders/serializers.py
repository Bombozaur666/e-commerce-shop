from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class StatisticSerializer(Serializer):
    product__name = CharField()
    quantity = IntegerField()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class OrderSerializer(ModelSerializer):
    client = UserSerializer()

    class Meta:
        model = Order
        fields = ['client', 'address', 'city', 'postal_code', 'created', 'payment']


class OrderItemSerializer(ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']
