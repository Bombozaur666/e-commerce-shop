from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, CharField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class CreateClientUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]
