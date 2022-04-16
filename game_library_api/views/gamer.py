from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Gamer


class GamerView(ViewSet):
    def create(self, request):
        gamer = Gamer.objects.get(pk=pk)
        gamer = Gamer()
        gamer.label = request.data["user"]

        try:
            gamer.save()
            serializer = GamerSerializer(
                gamer, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            gamer = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(
                gamer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        categories = Gamer.objects.all()
        serializer = GamerSerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        Arguments:
            serializers
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user')
