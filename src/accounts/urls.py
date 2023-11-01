from django.urls import path
from .views import CreateUserView, ProfileView

app_name = "users"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create-client-user"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
]
