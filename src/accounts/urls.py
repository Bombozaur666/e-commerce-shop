from django.urls import path
from .views import CreateUserView, ProfileView, ProductsListView, WishListView, WishListAdd, WishlistDelete
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create/", CreateUserView.as_view(), name="create-client-user"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("profile/orders/", ProductsListView.as_view(), name="user-profile"),
    path("profile/wishlist/list/", WishListView.as_view(), name="wishlist-list"),
    path("profile/wishlist/add/<int:pk>/", WishListAdd.as_view(), name="wishlist-add"),
    path("profile/wishlist/remove/<int:pk>/", WishlistDelete.as_view(), name="wishlist-del"),
]
