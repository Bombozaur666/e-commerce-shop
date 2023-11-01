from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from shared.permissions import IsSeller


# Create your views here.
class ListCategoriesView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"


class AddCategoryView(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsSeller]


class DeleteCategoryView(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsSeller]


class ModifyCategoryView(UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsSeller]
