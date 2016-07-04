from django.contrib.auth.models import User, Group
from quickstart.serializers import UserSerializer, GroupSerializer, MentionSerializer, PlaceSerializer, FriendSerializer, ReputationSerializer, FavoriteSerializer, TokenSerializer
from mentions.models import Mention
from friends.models import Friend
from favorites.models import Favorite
from reputations.models import Reputation
from places.models import Place
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import filters
import django_filters

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'mentions': reverse('mention-list', request=request, format=format),
        'friends': reverse('friend-list', request=request, format=format),
        'places': reverse('place-list', request=request, format=format),
        'reputations': reverse('reputation-list', request=request, format=format),
        'favorites': reverse('favorite-list', request=request, format=format),         
        'tokens': reverse('token-list', request=request, format=format)

    })


class TokenList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        tokens = Token.objects.all()
        serializer = TokenSerializer(tokens, many=True, context={'request': request})
        return Response(serializer.data)



class UserList(generics.ListAPIView):
    serializer_class = UserSerializer  

    """
    List all snippets, or create a new snippet.
    """


    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = User.objects.all()

        username = self.request.query_params.get('username', None)
        id = self.request.query_params.get('id', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        if id is not None:
            queryset = queryset.filter(id=id)      
       
        return queryset




class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GroupList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MentionLatFilter(django_filters.FilterSet):
    # example http://127.0.0.1:8000/mentions/?lat_minus=38&lat_plus=48&lng_minus=-84&lng_plus=-64
   # http://127.0.0.1:8000/mentions/?placename=bills&lat_minus=38&lat_plus=48&lng_minus=-84&lng_plus=-64
    lat_minus = django_filters.NumberFilter(name="lat", lookup_type='gte')
    lat_plus = django_filters.NumberFilter(name="lat", lookup_type='lte')
    lng_minus = django_filters.NumberFilter(name="lng", lookup_type='gte')
    lng_plus = django_filters.NumberFilter(name="lng", lookup_type='lte')
    lat = django_filters.NumberFilter(name="lat")
    lng = django_filters.NumberFilter(name="lng")
    placename = django_filters.filters.CharFilter(name="placename")

    class Meta:
        model = Mention
        fields = ['lat_minus', 'lat_plus', 'lng_minus', 'lng_plus', 'placename', 'lat', 'lng']


class MentionList(generics.ListAPIView):
    serializer_class = MentionSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = MentionLatFilter           
    """
    List all snippets, or create a new snippet.
    """
    """
    def get(self, request, format=None):
        mentions = Mention.objects.all()
        serializer = MentionSerializer(mentions, many=True)
        return Response(serializer.data)
    """

    def post(self, request, format=None):
        serializer = MentionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


    def get_queryset(self):
        queryset = Mention.objects.all()
        ordering_fields = ('created_date') 
        placeid = self.request.query_params.get('placeid', None)
        if placeid is not None:
            queryset = queryset.filter(placeid=placeid)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)  

        hashtags = self.request.query_params.get('hashtags', None)      
        if hashtags is not None:
            hashtag_filter = self.request.query_params.get('hashtags', None)
            queryset = Mention.objects.filter(hashtags__tagname=hashtag_filter)

        return queryset




class MentionDetail(generics.ListAPIView):
    serializer_class = MentionSerializer 
    """
    Retrieve, update or delete a mention instance.
    """
    def get_object(self, pk):
        try:
            return Mention.objects.get(pk=pk)
        except Mention.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mention = self.get_object(pk)
        serializer = MentionSerializer(mention)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mention = self.get_object(pk)
        serializer = MentionSerializer(mention, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mention = self.get_object(pk)
        mention.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class FriendList(generics.ListAPIView):
    serializer_class = FriendSerializer
    """
    List all snippets, or create a new snippet.
    """
    
    def post(self, request, format=None):
        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Friend.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        friendswith = self.request.query_params.get('friendswith', None)      
        if friendswith is not None:
            queryset = queryset.filter(friendswith=friendswith)


        return queryset
     

class FriendDetail(generics.ListAPIView):
    serializer_class = FriendSerializer
    """
    Retrieve, update or delete a mention instance.
    """
    def get_object(self, pk):
        try:
            return Friend.objects.get(pk=pk)
        except Friend.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        friend = self.get_object(pk)
        serializer = FriendSerializer(friend, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        friend = self.get_object(pk)
        serializer = FriendSerializer(friend, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        friend = self.get_object(pk)
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReputationList(generics.ListAPIView):
    serializer_class = ReputationSerializer
    """
    List all snippets, or create a new snippet.
    """
    
    def post(self, request, format=None):
        serializer = ReputationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Reputation.objects.all()

        authorname = self.request.query_params.get('authorname', None)
        if authorname is not None:
            queryset = queryset.filter(authorname=authorname)

        mentionid = self.request.query_params.get('mentionid', None)
        if mentionid is not None:
            queryset = queryset.filter(mentionid=mentionid) 
        
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author=author) 

        return queryset
     

class ReputationDetail(generics.ListAPIView):
    serializer_class = ReputationSerializer
    """
    Retrieve, update or delete a mention instance.
    """
    def get_object(self, pk):
        try:
            return Reputation.objects.get(pk=pk)
        except Reputation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        reputation = self.get_object(pk)
        serializer = ReputationSerializer(reputation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        reputation = self.get_object(pk)
        serializer = ReputationSerializer(reputation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        reputation = self.get_object(pk)
        reputation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class FavoriteList(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    """
    List all snippets, or create a new snippet.
    """
    
    def post(self, request, format=None):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Favorite.objects.all()
        userid = self.request.query_params.get('userid', None)
        placid = self.request.query_params.get('placid', None)
        if userid is not None:
            queryset = queryset.filter(userid=userid)
        
        if placid is not None:
            queryset = queryset.fiter(placid=placid)    
        
        return queryset
     

class FavoriteDetail(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    """
    Retrieve, update or delete a mention instance.
    """
    def get_object(self, pk):
        try:
            return Favorite.objects.get(pk=pk)
        except Favorite.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        favorite = self.get_object(pk)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        favorite = self.get_object(pk)
        serializer = FavoriteSerializer(favorite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        favorite = self.get_object(pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class PlaceLatFilter(django_filters.FilterSet):
    # example http://127.0.0.1:8000/mentions/?lat_minus=38&lat_plus=48&lng_minus=-84&lng_plus=-64
   # http://127.0.0.1:8000/mentions/?placename=bills&lat_minus=38&lat_plus=48&lng_minus=-84&lng_plus=-64
    lat_minus = django_filters.NumberFilter(name="lat", lookup_type='gte')
    lat_plus = django_filters.NumberFilter(name="lat", lookup_type='lte')
    lng_minus = django_filters.NumberFilter(name="lng", lookup_type='gte')
    lng_plus = django_filters.NumberFilter(name="lng", lookup_type='lte')
    lat = django_filters.NumberFilter(name="lat")
    lng = django_filters.NumberFilter(name="lng")
    placename = django_filters.filters.CharFilter(name="placename")

    class Meta:
        model = Place
        fields = ['lat_minus', 'lat_plus', 'lng_minus', 'lng_plus', 'placename', 'lat', 'lng']



class PlaceList(generics.ListAPIView):
    serializer_class = PlaceSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = PlaceLatFilter       
    """
    List all snippets, or create a new snippet.
    """
    
    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Place.objects.all()
        placeid = self.request.query_params.get('placeid', None)
        if placeid is not None:
            queryset = queryset.filter(placeid=placeid)
           
        
        return queryset
     

class PlaceDetail(generics.ListAPIView):
    serializer_class = PlaceSerializer
    """
    Retrieve, update or delete a mention instance.
    """
    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = self.get_object(pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
