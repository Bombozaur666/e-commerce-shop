from django.urls import path
from .views import (
    ListCategoriesView,
    CategoryView,
    AddCategoryView,
    DeleteCategoryView,
    ModifyCategoryView,
)

app_name = "categories"

urlpatterns = [
    path("list/", ListCategoriesView.as_view(), name="list-categories"),
    path("create/", AddCategoryView.as_view(), name="add-category"),
    path("<int:pk>/", CategoryView.as_view(), name="retrieve-category"),
    path("<int:pk>/delete/", DeleteCategoryView.as_view(), name="delete-category"),
    path("<int:pk>/update/", ModifyCategoryView.as_view(), name="update-category"),
]
