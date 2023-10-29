from django.urls import path
from .views import CreateOrderView, OrderStatisticView

app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('statistics/', OrderStatisticView.as_view(), name='order-statistic'),
]
