from django.conf.urls import url
from .views.follow_user import FollowUserView, FollowUserDetailView
from .views.follow_tag import FollowTagView, FollowTagDetialView

urlpatterns = [

    # user follow user
    url(r'^follow_user/(?P<user_id>[\d]+)$', FollowUserView.as_view()),
    url(r'^follow_user/detail/(?P<follow_id>[\d]+)$', FollowUserDetailView.as_view()),

    # user follow tag
    url(r'^follow_tag/(?P<user_id>[\d]+)$', FollowTagView.as_view()),
    url(r'^follow_tag/detail/(?P<follow_id>[\d]+)$', FollowTagDetialView.as_view()),

]
