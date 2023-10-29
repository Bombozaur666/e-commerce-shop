from django.urls import path
from .views import ListProductsView, ProductView

app_name = 'orders'

urlpatterns = [
    #path('add/', views.add, name='add'),
    path('list/', ListProductsView.as_view(), name='list-products'),
    path('<int:pk>/', ProductView.as_view(), name='retrieve-product'),
]