from django.urls import path
from .views import visitorList,visitorDetail,youtubedownloader

urlpatterns = [
    path('downloader', youtubedownloader),
    path('visitor', visitorList.as_view(), name='List of visitors'),
    path('visitor/<int:pk>', visitorDetail.as_view(), name='Single visitor data'),
]
