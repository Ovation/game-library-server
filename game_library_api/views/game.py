from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Gamer, Game, Category
from django.contrib.auth.models import User
from game_library_api.views import CategorySerializer


class GameView(ViewSet):
    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        game = Game()
        game.gamer = gamer
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.category = category
        try:
            game.save()
            serializer = GameSerializer(
                game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


def destroy(self, request, pk=None):

    try:
        game = Game.objects.get(pk=pk)
        game.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    except Game.DoesNotExist as ex:
        return Response({'message': ex.args[0]},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'message': ex.args[0]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def list(self, request):

    game = Game.objects.all()
    gamer = Gamer.objects.get(user=request.auth.user)
    category = self.request.query_params.get('catergory_id', None)
    serializer = GameSerializer(
        game, many=True, context={'request': request})
    return Response(serializer.data)


class GamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        Arguments:
            serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')


class GameSerializer(serializers.ModelSerializer):

    gamer = GamerSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'gamer', 'title', 'category', 'description',
                  'date', 'category')
