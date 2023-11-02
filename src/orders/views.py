import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Order, OrderItem
from django_filters import rest_framework as filters
from django.db.models import Sum
from products.models import Product
from shared.permissions import IsClient, IsSeller


class CreateOrderView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    def create(self, request):
        from django.core.mail import EmailMessage
        from django.conf import settings
        from json import loads

        order = Order(
            client=request.user,
            address=request.data["address"],
            city=request.data["city"],
            postal_code=request.data["postal_code"],
        )
        try:
            order.full_clean()
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order.save()

        order_list = loads(request.data["order"])
        bulk = []
        receivable = 0
        for _order in order_list:
            product = get_object_or_404(Product, pk=_order["product"])
            quantity = int(_order["quantity"])
            order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.price)
            try:
                order_item.full_clean()
            except ValidationError:
                order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            bulk.append(order_item)
            receivable += quantity * product.price

        OrderItem.objects.bulk_create(bulk)

        subject = f"Your Order: {order.pk} has been registered."
        message = f"Total sum of your order: {receivable}."
        from_email = settings.EMAIL_HOST_USER
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[order.client.email],
        )
        email.send()

        return Response(
            data={"receivable": receivable, "date of payment": order.date_of_payment},
            status=status.HTTP_201_CREATED,
        )


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact"],
            "description": ["exact"],
            "price": ["lte", "gte", "exact"],
        }


class OrderStatisticView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        if self.request.query_params.get("date_start"):
            start_date = self.request.query_params.get("date_start")
        else:
            start_date = datetime.datetime(year=2010, month=1, day=1)
        if self.request.query_params.get("date_end"):
            end_date = self.request.query_params.get("date_end")
        else:
            end_date = datetime.datetime.now()
        if self.request.query_params.get("limit"):
            limit = int(self.request.query_params.get("limit"))
        else:
            limit = None

        queryset = (
            OrderItem.objects.filter(order__created__range=(start_date, end_date))
            .values("product__name")
            .annotate(the_amount=Sum("quantity"))
            .order_by("-the_amount")[:limit]
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = list(self.filter_queryset(self.get_queryset()))
        return Response(queryset, status=status.HTTP_200_OK)
