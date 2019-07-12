from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from v1.posts.models.post import Post
from v1.posts.models.post_image import PostImage
from v1.posts.serializers.post_image import PostImageSerializer
from v1.accounts.models.user import User

class PostImageDetailAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def post(self, serializer):
        serializer = PostImageSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(PostImageSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        serializer = PostImageSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            self.update(request, *args, **kwargs)
            return Response(PostImageSerializer(serializer.instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        serializer = PostImageSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            self.destroy(request, *args, **kwargs)
            return Response(PostImageSerializer(serializer.instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
