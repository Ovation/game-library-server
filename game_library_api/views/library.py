from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Gamer, Game, Library
from django.contrib.auth.models import User


class LibraryView(ViewSet):
    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        library = Library()
        library.game = game
        library.gamer = gamer
        library.isFavorite = request.data["isFavorite"]

        try:
            library.save()
            serializer = LibrarySerializer(
                library, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            library = Library.objects.get(pk=pk)
            serializer = LibrarySerializer(
                library, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        game = Game.objects.get(pk=request.data["game"])
        gamer = Gamer.objects.get(user=request.auth.user)

        library = Library.objects.get(pk=pk)
        library.game = game
        library.gamer = gamer
        library.isFavorite = request.data["isFavorite"]
        library.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            library = Library.objects.get(pk=pk)
            library.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        library = Library.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)

        game = self.request.query_params.get('game_id', None)
        if game is not None:
            library = library.filter(post__id=game)

        serializer = LibrarySerializer(
            library, many=True, context={'request': request})
        return Response(serializer.data)


class LibraryUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class LibraryGamerSerializer(serializers.ModelSerializer):

    user = LibraryUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'gamer', 'title', 'category',
                  'date', 'description',)
