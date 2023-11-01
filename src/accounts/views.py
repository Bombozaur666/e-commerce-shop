from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CreateClientUserSerializer
from shared.utils import Roles


# Create your views here.


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateClientUserSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
        )
        group = Group.objects.get(name=Roles.CLIENT)
        user.save()
        user.groups.add(group)
        serializer = CreateClientUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
