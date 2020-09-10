from django.shortcuts import render
from django.http import JsonResponse
from simpleApp.models import Posts
from django.views.decorators.csrf import csrf_exempt
from simpleApp.serializers import PostsSerializer

from math import radians, cos, sin, asin, sqrt

# Create your views here.

@csrf_exempt
def add(request):
    try:
        name = request.POST["name"]
        lat = request.POST["latitude"]
        long= request.POST["longitude"]
        post = Posts(name=request.POST["name"], loc={"type":"Point" , "coordinates": [long,lat] })
        post.save()
        return JsonResponse({"task" :"Inserted"})
    except Exception as e:
        print(e)
        return JsonResponse({"task" : "failure"})

@csrf_exempt
def search(request):
    try:
        ret_data=[]
        radius = int(request.POST["radius"])
        lat = float(request.POST["latitude"])
        long = float(request.POST["longitude"])
        all_data = Posts.objects.all()
        center_point = [{'lat': lat, 'lng': long}]
        for data in all_data:
            reqQuery = dict(data.loc)
            coordinates = reqQuery["coordinates"]
            test_point = [{'lat':float(coordinates[1]), 'lng':float(coordinates[0])}]
            lat1 = center_point[0]['lat']
            lon1 = center_point[0]['lng']
            lat2 = test_point[0]['lat']
            lon2 = test_point[0]['lng']
            kmDistance = distancePoint(lon1, lat1, lon2, lat2)
            if kmDistance <= radius:
                infoDict = PostsSerializer(data).data
                infoDict["distance"] =str(kmDistance) + " Km"
                ret_data.append(infoDict)
        print(ret_data)
        return JsonResponse({"task" :"done" , "data": ret_data})
    except Exception as e:
        print(e)
        return JsonResponse({"task" : "failure"})


def distancePoint(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r
