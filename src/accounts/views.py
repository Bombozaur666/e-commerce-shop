from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from orders.serializers import OrderSerializer
from .serializers import CreateClientUserSerializer, UserSerializer
from shared.utils import Roles
from orders.models import Order
from products.serializers import WishListSerializer
from products.models import WishList, Product


# Create your views here.


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateClientUserSerializer

    def create(self, request, *args, **kwargs):
        if not (
            request.POST.get("username")
            and request.POST.get("password")
            and request.POST.get("first_name")
            and request.POST.get("last_name")
            and request.POST.get("email")
        ):
            return Response({"error": "Your data is incorrect."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if User.objects.filter(username=request.POST.get("username")):
            return Response(
                {"error": "There is already user with this username."}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user = User(
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
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

        subject = "Account Created"
        message = f"Your account '{user.username}' has beem created. Welcome {user.get_full_name()}"
        from_email = settings.EMAIL_HOST_USER
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[user.email],
        )
        try:
            email.send()
        except SMTPException:
            pass
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


class WishListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get_queryset(self):
        queryset = WishList.objects.filter(client=self.request.user).all()
        return queryset


class WishListAdd(CreateAPIView):
    model = WishList
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.kwargs["pk"])
        wish = WishList(client=request.user, product=product)
        wish.save()
        return Response(status=status.HTTP_201_CREATED)


class WishlistDelete(DestroyAPIView):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs["pk"])
        queryset = WishList.objects.filter(client=self.request.user, product=product).all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset()
        instance.delete()
        return Response(status=status.HTTP_200_OK)
