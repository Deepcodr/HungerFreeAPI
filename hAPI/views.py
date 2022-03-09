from django.shortcuts import render
import rest_framework
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse,JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from hAPI.models import Request,donation,UserData
from hAPI.serializers import RequestSerializer,donationSerializer,UserDataSerializer
# Create your views here

@csrf_exempt
def donations(request,id=0):
    if request.method=='GET':
        lat=request.GET.get('lat',40.731)
        lng=request.GET.get('lng',-73.997)
        minlat=float(lat)-0.060
        minlng=float(lng)-0.060
        maxlat=float(lat)+0.060
        maxlng=float(lng)+0.060
        requests_data=Request.objects.filter(Lat__range=[minlat,maxlat],Lng__range=[minlng,maxlng])
        requests_datacount=Request.objects.filter(Lat__range=[minlat,maxlat],Lng__range=[minlng,maxlng]).count()
        if requests_datacount==0:
            return JsonResponse("No requests found for this location",safe=False)
        else:
            requests_serializer=RequestSerializer(requests_data,many=True)
            return JsonResponse(requests_serializer.data,safe=False)
    elif request.method=='POST':
        donation_data=JSONParser().parse(request)
        donation_serializer_data=donationSerializer(data=donation_data)
        if donation_serializer_data.is_valid():
            donation_serializer_data.save()
            return HttpResponse(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method=='DELETE':
        delLat=request.GET.get('delLat',None)
        delLng=request.GET.get('delLng',None)
        acceptUID=request.GET.get('uid',None)
        
        if(delLat!=None and delLng!=None):
            donation_data=donation.objects.filter(Lat=delLat,Lng=delLng)[0]
            createUID=donation_data.UserID
            if(acceptUID!=createUID):
                user_data= UserData.objects.create(Type='D',create_name=donation_data.Name,create_uid=createUID,accept_uid=acceptUID,Lat=donation_data.Lat,Lng=donation_data.Lng)
                user_data.save()
                donation_data.delete()
                return JsonResponse("Donation Accepted Successfully",safe=False)
            else:
                return JsonResponse("You Cannot Accept Your Own donation",safe=False)
        else:
            return JsonResponse("Cannot Accept Donation",safe=False)


@csrf_exempt
def requests(request,id=0):
    if request.method=='GET':
        lat=request.GET.get('lat',40.731)
        lng=request.GET.get('lng',-73.997)
        minlat=float(lat)-0.060
        minlng=float(lng)-0.060
        maxlat=float(lat)+0.060
        maxlng=float(lng)+0.060
        donations_data=donation.objects.filter(Lat__range=[minlat,maxlat],Lng__range=[minlng,maxlng])
        donation_datacount=donation.objects.filter(Lat__range=[minlat,maxlat],Lng__range=[minlng,maxlng]).count()
        if donation_datacount==0:
            return JsonResponse("No donations found for this location",safe=False)
        else:
            donations_serializer=donationSerializer(donations_data,many=True)
            return JsonResponse(donations_serializer.data,safe=False)
    elif request.method=='POST':
        request_data=JSONParser().parse(request)
        request_serializer=RequestSerializer(data=request_data)
        if request_serializer.is_valid():
            request_serializer.save()
            return HttpResponse(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method=='DELETE':
        #getting url data
        delLat=request.GET.get('delLat',None)
        delLng=request.GET.get('delLng',None)
        acceptUID=request.GET.get('uid',None)

        if(delLat!=None and delLng!=None):
            request_data=Request.objects.filter(Lat=delLat,Lng=delLng)[0]
            createUID=request_data.UserID
            if(createUID!=acceptUID):
                user_data= UserData.objects.create(Type='R',create_name=request_data.Name,create_uid=createUID,accept_uid=acceptUID,Lat=request_data.Lat,Lng=request_data.Lng)
                user_data.save()
                request_data.delete()
                return JsonResponse("Request Accepted Successfully",safe=False)
            else:
                return JsonResponse("You Cannot Accept Your Own Request",safe=False)
        else:
            return JsonResponse("Cannot Accept Request",safe=False)

@csrf_exempt
def getuserdata(request,id=0):
    if request.method=='GET':
        uid=request.GET.get('uid',None)
        gettype=request.GET.get('get',None)
        
        if(uid!=None):
            if gettype=='101':
                user_data=Request.objects.filter(UserID=uid)
                serialized_userdata=RequestSerializer(user_data,many=True)
                return JsonResponse(serialized_userdata.data,safe=False)                
            elif gettype=='102':
                user_data=donation.objects.filter(UserID=uid)
                serialized_userdata=donationSerializer(user_data,many=True)        
                return JsonResponse(serialized_userdata.data,safe=False)        
            elif gettype=='103':
                user_data=UserData.objects.filter(Type='R',accept_uid=uid)
                serialized_userdata=UserDataSerializer(user_data,many=True)        
                return JsonResponse(serialized_userdata.data,safe=False)
            elif gettype=='104':
                user_data=UserData.objects.filter(Type='D',accept_uid=uid)
                serialized_userdata=UserDataSerializer(user_data,many=True)        
                return JsonResponse(serialized_userdata.data,safe=False)        
            elif gettype=='105':
                user_data=UserData.objects.filter(create_uid=uid)
                serialized_userdata=UserDataSerializer(user_data,many=True)        
                return JsonResponse(serialized_userdata.data,safe=False)       
        else:
            return JsonResponse("No Data Found",safe=False)
    elif request.method=='DELETE':
        uid=request.GET.get('uid',None)
        if(uid!=None):
            user_data=UserData.objects.filter(create_uid=uid)
            user_data.delete()
            return JsonResponse("History Cleared",safe=False)
        else:
            return JsonResponse("Cannot Clear History",safe=False)