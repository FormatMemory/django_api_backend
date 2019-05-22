from django.conf.urls import url
from .views.post_vote import PostVoteView, PostVoteDetail
from .views.post_reply_vote import PostReplyVoteView, PostReplyVoteDetail


urlpatterns = [

    # Post votes
    url(r'^post_votes$', PostVoteView.as_view()),
    url(r'^post_votes/(?P<post_vote_id>[\d]+)$', PostVoteDetail.as_view()),

    # Post Reply votes
    url(r'^post_reply_votes$', PostVoteView.as_view()),
    url(r'^post_reply_votes/(?P<post_vote_id>[\d]+)$', PostVoteDetail.as_view()),
]
