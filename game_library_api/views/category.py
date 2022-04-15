from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Category, Game


class CategoryView(ViewSet):
    def create(self, request):
        category = Category.objects.get(pk=pk)
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        Arguments:
            serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
