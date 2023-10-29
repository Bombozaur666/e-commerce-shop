from django.urls import path
from .views import ListProductsView, ProductView, AddProductView, DeleteProductView, ModifyProductView

app_name = 'orders'

urlpatterns = [
    path('list/', ListProductsView.as_view(), name='list-products'),
    path('create/', AddProductView.as_view(), name='list-products'),
    path('<int:pk>/', ProductView.as_view(), name='retrieve-product'),
    path('<int:pk>/delete/', DeleteProductView.as_view(), name='retrieve-product'),
    path('<int:pk>/update/', ModifyProductView.as_view(), name='retrieve-product'),
]