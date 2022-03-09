from rest_framework import serializers
from hAPI.models import donation,Request,UserData

class donationSerializer(serializers.ModelSerializer):
    class Meta:
        model=donation
        fields=('Name','UserID','Email','Place_id','Lat','Lng')

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Request
        fields=('Name','UserID','Email','Place_id','Lat','Lng')

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserData
        fields=('Type','create_name','create_uid','accept_uid','Lat','Lng')