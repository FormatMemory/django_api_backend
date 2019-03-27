from django.urls import path

from user import views


app_name = "user"
userListView = views.UserListView.as_view({'get': 'list'})

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("user_list", userListView, name="user_list"),
    path("delete_token", views.DeleteTokenView.as_view(), name="delete_token"),
]
