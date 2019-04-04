from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.categories.models.category import Category
from v1.categories.serializers.category import CategorySerializer, CategorySerializerCreate, CategorySerializerUpdate, CategoryFullSerializer
from v1.utils.permissions import is_administrator

# categories/
class CategoryView(APIView):
    @staticmethod
    def get(request):
        """
        See category list
        """

        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)


    @staticmethod
    def post(request):
        """
        Create a category
        """
      
        serializer = CategorySerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(CategorySerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# categories/{category_id}
class CategoryDetail(APIView):
    @staticmethod
    def get(request, category_id):
        """
        View individual category and it contains posts
        """

        category = get_object_or_404(Category, pk=category_id)
        print(category)
        return Response(CategoryFullSerializer(category).data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, category_id):
        """
        Update category
        """

        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializerUpdate(category, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CategorySerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, category_id):
        """
        Delete category
        """
        if not is_administrator(request.user):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
