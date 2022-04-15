from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Gamefacts, Gamefacts, Game


class GameFactsView(ViewSet):
    def create(self, request):
        game = Game.objects.get(pk=request.data["game"])
        facts = Gamefacts.objects.get(pk=pk)
        facts = Gamefacts()
        facts.fact = request.data["fact"]
        facts.game = game

        try:
            facts.save()
            serializer = FactSerializer(
                facts, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            facts = Gamefacts.objects.get(pk=pk)
            serializer = FactSerializer(
                facts, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        facts = Gamefacts.objects.all()
        serializer = FactSerializer(
            facts, many=True, context={'request': request})
        return Response(serializer.data)


class FactSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        Arguments:
            serializers
    """
    class Meta:
        model = Gamefacts
        fields = ('id', 'fact', 'game')
