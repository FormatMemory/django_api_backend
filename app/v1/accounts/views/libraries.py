from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.accounts.models.libraries import Library, LibraryItem
from v1.accounts.serializers.libraries import LibrarySerializer, LibraryItemSerializer, LibraryDetailSerializer, LibraryCreateSerializer, \
                                              LibrarySerializerUpdate, LibraryItemSerializerUpdate, LibraryItemCreateSerializer
from v1.accounts.serializers.user import UserSerializerLogin
from v1.filters.libraries.library import library_filter


# libraries
class LibraryView(APIView):

    @staticmethod
    def get(request):
        """
        List libraries
        """

        libraries = Library.objects.all()
        libraries = library_filter(request, libraries)
        # paginate_by = 10
        try:
            if 'order_by' in request.query_params:
                libraries.order_by(request.query_params['order_by'])
            if 'limit' in request.query_params:
                libraries = libraries[:int(request.query_params['limit'])]
            if type(libraries) == Response:
                return libraries
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(LibrarySerializer(libraries, many=True).data)

    @staticmethod
    def post(request):
        """
        Create a library
        """
        serializer = LibraryCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(LibraryCreateSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# libraries/{library_id}
class LibraryDetailView(APIView):


    @staticmethod
    def get(request, library_id):
        """
        View individual library
        """
        library = get_object_or_404(Library, pk=library_id)
        return Response(LibraryDetailSerializer(library).data)

    @staticmethod
    def patch(request, library_id):
        """
        Update library
        """

        library = get_object_or_404(Library, pk=library_id)
        if library.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = LibrarySerializerUpdate(library, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(LibrarySerializerUpdate(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, library_id):
        """
        Delete library
        """

        library = get_object_or_404(Library, pk=library_id)
        if library.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        library.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @staticmethod
    def post(request, library_id):
        """
        Create a library_item_item under library_id
        """

        library = get_object_or_404(Library, pk=library_id)
        if library.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = LibraryItemCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            library_item = serializer.save()
            library_item.update(library=library)
            library_item.save()
            return Response(LibraryCreateSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# libraries/{library_id}/{library_item_id}
class LibraryItemDetailView(APIView):


    @staticmethod
    def get(request, library_item_id):
        """
        View individual library_item
        """
        library_item = get_object_or_404(LibraryItem, pk=library_item_id)
        return Response(LibraryItemSerializer(library_item).data)


    @staticmethod
    def patch(request, library_item_id):
        """
        Update library_item
        """

        library_item = get_object_or_404(LibraryItem, pk=library_item_id)
        if library_item.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = LibraryItemSerializerUpdate(library_item, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(LibraryItemSerializerUpdate(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, library_item_id):
        """
        Delete library_item
        """

        library_item = get_object_or_404(Library, pk=library_item_id)
        if library_item.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        library_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)