from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from mentions.models import  Mention,  Hashtag 
from friends.models import Friend
from favorites.models import Favorite
from reputations.models import Reputation
from places.models import Place
from rest_framework import serializers
from rest_framework.decorators import api_view
import time
from django.db import models 
from django.forms.models import model_to_dict



class TokenSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Token


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
  

#class TrackSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Track
        #fields = ('order', 'title', 'duration')

class HashListingFieldSerializer(serializers.RelatedField):  
    def to_internal_value(self, data):
        tagname = data
        return {
            'tagname': tagname
        }
    def to_representation(self, value):
        return value.tagname


class PlacesCountSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return (value.mention_count)   



class PlaceSerializer(serializers.ModelSerializer):
    #mentions = MentionSerializer(read_only=True, source="mention_set", many=True)
    mention_count = serializers.IntegerField(source='mention_set.count', read_only=True)
    favorite_count = serializers.IntegerField(source='favorite_set.count', read_only=True)    
    class Meta:
        model = Place
        fields = ('id', 'placename', 'placecity', 'mention_count', 'favorite_count', 'lat', 'lng', 'created_date', 'published_date') 
    
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PlaceSerializer, self).__init__(*args, **kwargs)

class MentionSerializer(serializers.ModelSerializer):
    hashtags = HashListingFieldSerializer(many=True, queryset=Hashtag.objects.all())
    placecountid = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), source='placeinfo', write_only=True)    
    placeinfo = PlaceSerializer(read_only=True)
    class Meta:
        model = Mention
        fields = ('id', 'author', 'hashtags', 'username', 'placeid', 'placecountid', 'placeinfo', 'lat', 'lng', 'placemention', 'created_date', 'published_date')  

    def create(self, validated_data):
        tags_data = validated_data.pop('hashtags')
        mention = Mention.objects.create(**validated_data)        
        for tags_data in tags_data:
            Hashtag.objects.create(mention=mention, **tags_data)
        return mention


    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(MentionSerializer, self).__init__(*args, **kwargs)



class ReputationSerializer(serializers.ModelSerializer):
    mention = MentionSerializer()
    mentionid = serializers.PrimaryKeyRelatedField(queryset=Mention.objects.all(), source='mention', write_only=True)

    class Meta:
        model = Reputation
        fields = ('id', 'author',  'authorname', 'value', 'mentionid', 'placeid', 'mention', 'created_date', 'published_date')  

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ReputationSerializer, self).__init__(*args, **kwargs)

class FriendSerializer(serializers.ModelSerializer):
    friendswith = UserSerializer()
    class Meta:
        model = Friend    
        fields = ('id', 'username', 'friendswith', 'created_date', 'published_date')         

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(FriendSerializer, self).__init__(*args, **kwargs)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'userid', 'placename', 'placeid')

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(FavoriteSerializer, self).__init__(*args, **kwargs)


     