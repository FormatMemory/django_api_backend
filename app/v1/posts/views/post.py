from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from v1.filters.posts.post import post_filter
from v1.posts.models.post import Post
from v1.posts.serializers.post import PostSerializer, PostSerializerCreate, PostSerializerFull, PostSerializerUpdate
from v1.user_page_views.models.user_page_view import UserPageView
from v1.accounts.models.user import User

from datetime import datetime

class PostPagination(PageNumberPagination):
    page_size = 1

#posts
class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination




# posts
# class PostView(APIView):

#     pagination_class = PostPagination

#     @staticmethod
#     def get(request):
#         """
#         List posts
#         """
#         posts = Post.objects.all()
#         posts = post_filter(request, posts)
#         paginate_by = 1
#         try:
#             if 'order_by' in request.query_params:
#                 posts.order_by(request.query_params['order_by'])
#             if 'limit' in request.query_params:
#                 posts = posts[:int(request.query_params['limit'])]
#             if type(posts) == Response:
#                 return posts
#         except Exception:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(PostSerializer(posts, many=True).data)

#     @staticmethod
#     def post(request):
#         """
#         Create post
#         """

#         serializer = PostSerializerCreate(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(PostSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# posts/{post_id}
class PostDetail(APIView):

    @staticmethod
    def _record_view(request, post_id):
        """
        record post has get a view
        """
        post = get_object_or_404(Post, id=post_id)
        user_page_view, created = UserPageView.objects.get_or_create(post=post, ip=request.META['REMOTE_ADDR'], created=datetime.now().strftime('%Y-%m-%d %H:%M:00'))
        if created: 
            user_page_view.session=request.session.session_key
            user_page_view.user=request.user
            user_page_view.save()
                # user_page_view.save()
                # return HttpResponse(u"%s" % UserPageView.objects.filter(question=question).count())

    @staticmethod
    def get(request, post_id):
        """
        View individual post
        """
        post = get_object_or_404(Post, pk=post_id)
        PostDetail._record_view(request, post_id)
        return Response(PostSerializerFull(post).data)

    @staticmethod
    def patch(request, post_id):
        """
        Update post
        """

        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializerUpdate(post, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostSerializerFull(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, post_id):
        """
        Delete post
        """

        post = get_object_or_404(Post, pk=post_id)
        if post.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
