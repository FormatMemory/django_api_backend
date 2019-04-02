from django.conf.urls import url
from .views.user_page_view import UserPageViewView, UserPageViewDetail


urlpatterns = [

    # Post votes
    url(r'^user_page_views', UserPageViewView.as_view()),
    url(r'^user_page_views/(?P<user_id>[\d]+)$', UserPageViewDetail.as_view()),
]
