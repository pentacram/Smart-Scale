from threading import Thread
import serial
from django.utils import timezone
from .models import *
ser = serial.Serial('COM23',19200,timeout=1)

while True:
    new_data = ser.read(100)
    if new_data:
        new_data = new_data.decode('utf-8')
        new_data= new_data.split(',')
        current =InfoFields.objects.filter(number=new_data[0],weight=float(new_data[1][1:])).last()
        if current:
            def updating():
                InfoFields.objects.create(
                    number=new_data[0],
                    weight=float(new_data[1][1:]),
                    age=current.age,
                    gender=current.gender,
                    feed=current.feed,
                 
                    born_date=current.born_date
                )
            background_job = Thread(target=updating())
            background_job.start()
            print('ok')
        else:
            def creating():
                InfoFields.objects.create(
                    number=new_data[0],
                    weight=float(new_data[1][1:])
                )
            background_job = Thread(target=creating())
            background_job.start()
            print('ok')