from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from orders.serializers import OrderSerializer
from .serializers import CreateClientUserSerializer, UserSerializer
from shared.utils import Roles

from orders.models import Order


# Create your views here.


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateClientUserSerializer

    def create(self, request, *args, **kwargs):
        user = User(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
        )
        user.set_password(request.POST.get("password"))
        try:
            user.full_clean()
        except ValidationError:
            return Response({"error": "Your data is incorrect."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.get(name=Roles.CLIENT)
        user.save()
        user.groups.add(group)
        serializer = CreateClientUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(client=self.request.user)
        return queryset
