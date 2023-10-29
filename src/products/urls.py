from django.urls import path
from .views import ListProductsView

app_name = 'orders'

urlpatterns = [
    #path('add/', views.add, name='add'),
    path('list/', ListProductsView.as_view(), name='list-products'),
]