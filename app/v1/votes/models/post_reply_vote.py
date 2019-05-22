from django.db import models
from v1.replies.models.post_reply import PostReply
from v1.votes.models.vote import Vote


class PostReplyVote(Vote):
    post_reply = models.ForeignKey(PostReply, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'post_reply_votes'
        unique_together = ('post_reply', 'user')

    def __str__(self):
        return f'reply: {self.post_reply.id} - value: {self.value}'
