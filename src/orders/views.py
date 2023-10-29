from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer
from rest_framework.generics import CreateAPIView
from .models import Order, OrderItem
import json

from products.models import Product


class CreateOrderView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

        user_groups = list(self.request.user.groups.values_list('name', flat=True))
        if 'client' not in user_groups:
            self.permission_denied(request)

    def create(self, request):
        order = Order(client=request.user,
              address=request.data['address'],
              city=request.data['city'],
              postal_code=request.data['postal_code'])

        order.full_clean()
        order.save()

        order_list = json.loads(request.data['order'])
        bulk = []
        receivable = 0
        for _order in order_list:
            product = get_object_or_404(Product, pk=_order['product'])
            quantity = int(_order['quantity'])
            bulk.append(OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            ))
            receivable += quantity * product.price
        OrderItem.objects.bulk_create(bulk)
        return Response(data={"receivable": receivable, 'date of payment': order.date_of_payment},
                        status=status.HTTP_201_CREATED)






