from django.shortcuts import render
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework import generics
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from pytube import YouTube
from django.core.mail import EmailMessage


from .models import Visitor
from .serializer import Visitorserializer

# For Filter
from rest_framework.filters import SearchFilter
# Create your views here.


#List of Visitor and create 
class visitorList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset=Visitor.objects.all()
    serializer_class= Visitorserializer

    # Search
    filter_backends = [SearchFilter]
    search_fields = ['country_name','city']

#Details of Visitor and Update,Delete,IdSearch
class visitorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Visitor.objects.all()
    serializer_class= Visitorserializer



@csrf_exempt
def youtubedownloader(request):

    
    if request.method == 'POST':
        data = json.loads(request.body)
        video_link=data['link']
        yt = YouTube(video_link)

        info=[]
        audio=[]

        video=[
        {
            'Video Title':yt.title,
            'video_pic':yt.thumbnail_url,
        },
    ]
        for stream in yt.streams.filter(progressive=True):
            type=stream.mime_type
            res=stream.resolution

            links={
            'Type':type,
            'Resolution':res,
            'Link':stream.url
            }
            
            info.append(links)

        for sound in yt.streams.filter(only_audio=True):
            type=sound.mime_type
            res=sound.resolution

            links={
            'Type':type,
            'Resolution':res,
            'Link':stream.url
            }
            
            audio.append(links)

        #Get the IP Address of visitor who ask link in DataBase by making GET Method
        api_base=requests.get("https://freegeoip.app/json/")
        response=api_base.json()

        information={
            "ip": response["ip"],
            "country_code": response["country_code"],
            "country_name": response["country_name"],
            "time_zone": response["time_zone"],
            "latitude": response["latitude"],
            "longitude": response["longitude"],
            "ytd_request_link": video_link,
            "video_title": yt.title,
            "video_thumb_img": yt.thumbnail_url
            }

        #Insert the information in DataBase by making POST Method
        req_url="http://127.0.0.1:8000/ytd/visitor"
        if requests.post(req_url, json=information):
            print("Has been send!")
            
            #Sending the Email to Owner
            email_from="Youtube Request"
            email_to="ishimwejulespacis@gmail.com"
            subject_message="NEW YOUTUBE API Request ⚡"

            subject, from_email, to = subject_message, email_from, email_to 
            text_content = "<center style='border:solid red 2px;'><h1>⚡This Ip: "+information['ip']+"</h1>Request From:<h2>Video Thumbnail</h2><h2 style='color:red;'>"+yt.title+"</h2><img src="+yt.thumbnail_url+" width='200'><br/><h2>OTHER INFORMATION</h2><p><b>Country: </b>"+information['country_name']+"</p><p><b>Youtube Link: </b>"+information['ytd_request_link']+"</p><p><b>Ip on map Link: </b> <a href='https://www.google.com/maps/search/?api=1&query="+str(information['latitude'])+"%2C"+str(information['longitude'])+"' target='_blank'>MAP Link</a></p><p><b>Country code:  </b>"+information['country_code']+"</p><p><b>latitude:  </b>"+str(information['latitude'])+"</p><p><b>longitude:  </b>"+str(information['longitude'])+"</p><br><a href='https://www.shamigo.rw/' target='_blank'>Visit My Web</a></center>"
            msg = EmailMessage(subject, text_content, from_email, [to])
            msg.content_subtype = 'html'
            msg.send()
            print("E-mail Send")
            

            
        #return HttpResponse(info, content_type='text/json')
        return JsonResponse({'Info':video,'Download_videos': info,'Download_audios': audio}, content_type='text/json')
        
    return JsonResponse({'data': 'This Api use POST request only'})
