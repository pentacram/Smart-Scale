from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InfoFields(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    T_GENDER = (
        ("E", "Erkək"),
        ("D", "Dişi")
    )
    # Special_Case = (
    #     ("vitamin", "Vitamin"),
    #     ("derman", "Dərman")
    #
    # )
    # sira = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    # age = models.CharField(max_length=255)
    gender = models.CharField(max_length=55, choices=T_GENDER)
    breed = models.CharField(max_length=55)
    feed = models.CharField(max_length=55)
    special_case = models.CharField(max_length=100, null=True, blank=True)
    age = models.DateTimeField(null=True, blank=True)

    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

# class Select(models.Model):
#     variants = models.CharField(max_length=50, null=True)