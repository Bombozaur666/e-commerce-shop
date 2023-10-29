from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from .models import Product


# Create your views here.

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {'name': ['exact'],
                  'description': ['exact'],
                  'price': ['lte', 'gte', 'exact']
            }


class ListProductsView(ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    ordering_categories = ['name', 'category', 'price']

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')

        if category:
            queryset = queryset.filter(category__name__contains=category)

        ordering = self.request.query_params.get('ordering')
        if ordering in self.ordering_categories:
            queryset = queryset.order_by(ordering)
        return queryset
