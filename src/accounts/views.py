from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
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
        user = User(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        try:
            user.full_clean()
        except ValidationError:
            return Response({"error": "Your data is incorrect."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.get(name=Roles.CLIENT)
        user.save()
        user.groups.add(group)
        serializer = CreateClientUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
