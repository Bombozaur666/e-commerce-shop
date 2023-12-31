from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from shared.permissions import IsSeller
from .models import Product


# Create your views here.


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "contains"],
            "description": ["exact", "contains"],
            "price": ["lte", "gte", "exact"],
        }


class ListProductsView(ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    ordering_categories = ["name", "category", "price"]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(category__name__contains=category)

        ordering = self.request.query_params.get("ordering")
        if ordering in self.ordering_categories:
            queryset = queryset.order_by(ordering)
        return queryset


class ProductView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class AddProductView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsSeller]


class DeleteProductView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsSeller]


class ModifyProductView(UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsSeller]
