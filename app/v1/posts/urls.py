from django.conf.urls import url
from .views.post import PostListView, PostCreateAPIView, PostDetail
from .views.post_image import PostImageDetailAPIView


urlpatterns = [

    # Posts
    url(r'^posts/$', PostListView.as_view()),
    url(r'^posts_create/$', PostCreateAPIView.as_view()),
    url(r'^posts/(?P<post_id>[\d]+)$', PostDetail.as_view()),
    url(r'^post_image/(?P<pk>[\d]+)$', PostImageDetailAPIView.as_view()),

]
