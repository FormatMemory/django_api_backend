from django.contrib import admin
from .models.follow_user import FollowUser
from .models.follow_tag import FollowTag


admin.site.register(FollowUser)
admin.site.register(FollowTag)
