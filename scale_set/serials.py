import serial
from django.utils import timezone
from .models import *
ser = serial.Serial('COM1',9600)
ser.open()
while True:
    new_data = ser.read()
    if new_data:
        new_data= new_data.split(',')
        current =InfoFields.objects.filter(id=new_data[0],weight=new_data[1]).last()
        if current:
            InfoFields.objects.create(
                number = new_data[0],
                weight=new_data[1],
                age=current.age,
                gender=current.gender,
                feed =current.feed,
                born_date = current.born_date
            )
        else:
            InfoFields.objects.create(
                number=new_data[0],
                weight=new_data[1]
            )