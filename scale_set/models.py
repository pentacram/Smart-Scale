from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InfoFields(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    T_GENDER = (
        ("E", "Erkək"),
        ("D", "Dişi")
    )

    number = models.CharField(max_length=50, null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    gender = models.CharField(max_length=55, choices=T_GENDER,null=True,blank=True)
    breed = models.CharField(max_length=55,null=True,blank=True)
    feed = models.CharField(max_length=55,null=True,blank=True)
    special_case = models.CharField(max_length=100, null=True, blank=True)
    age = models.DateTimeField(null=True, blank=True)

    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

