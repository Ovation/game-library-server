from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from game_library_api.models import Gamer, Friendlist
from django.contrib.auth.models import User


class FriendlistView(ViewSet):
    def create(self, request):
        friend = Gamer.objects.get(pk=request.data["friend"])
        gamer = Gamer.objects.get(pk=request.data["gamer"])
        friendlist = Friendlist.objects.get(pk=pk)
        friendlist = Friendlist()
        friendlist.friend = friend
        friendlist.gamer = gamer

        try:
            friendlist.save()
            serializer = FactSerializer(
                friendlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            friendlist = Friendlist.objects.get(pk=pk)
            serializer = FactSerializer(
                friendlist, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        categories = Friendlist.objects.all()
        serializer = FactSerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class FactSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        Arguments:
            serializers
    """
    class Meta:
        model = Friendlist
        fields = ('id', 'gamer', 'friend', 'date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class GamerSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']
