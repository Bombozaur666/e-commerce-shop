from django.urls import path
from .views import CreateUserView, ProfileView, ProductsListView, WishListView, WishListAdd, WishlistDelete

app_name = "users"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create-client-user"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("profile/orders/", ProductsListView.as_view(), name="user-profile"),
    path("profile/wishlist/list/", WishListView.as_view(), name="wishlist-list"),
    path("profile/wishlist/add/<int:pk>/", WishListAdd.as_view(), name="wishlist-add"),
    path("profile/wishlist/remove/<int:pk>/", WishlistDelete.as_view(), name="wishlist-del"),
]
