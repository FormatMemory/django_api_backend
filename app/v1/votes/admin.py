from django.contrib import admin
from .models.post_vote import PostVote
from .models.post_reply_vote import PostReplyVote


admin.site.register(PostVote)
admin.site.register(PostReplyVote)
