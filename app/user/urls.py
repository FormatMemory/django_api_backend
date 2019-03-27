from django.urls import path

from user import views


app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("user_list", views.UserListView.as_view(), name="user_list"),
    path("delete_token", views.DeleteTokenView.as_view(), name="delete_token"),
]
