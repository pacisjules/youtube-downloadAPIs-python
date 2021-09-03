from django.db import models

# Create your models here.

# Model for visitor
class Visitor(models.Model):
    ip=models.CharField(max_length=50)
    video_title=models.CharField(max_length=250, null=True)
    video_thumb_img=models.CharField(max_length=250,null=True)
    country_code=models.CharField(max_length=11, null=True)
    country_name=models.CharField(max_length=250, null=True)
    time_zone=models.CharField(max_length=250, null=True)
    latitude=models.FloatField(max_length=200, null=True)
    longitude=models.FloatField(max_length=200, null=True)
    ytd_request_link=models.URLField(null=False)
    date_created=models.DateField(auto_now_add=True, null=True)
    time_created=models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ip


