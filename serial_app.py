import serial
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_scale.settings')
django.setup()
from django.utils import timezone
from scale_set.models import *
from .send_serial import send_string
import traceback

send = 'ok'
ser = serial.Serial('COM23',19200,timeout=1)
print("Connect success", ser)


while True:
    new_data = ser.read(100)
    try:
        if new_data:
            new_data = new_data.decode('utf-8')
            new_data= new_data.split(',')
            current =InfoFields.objects.filter(number=new_data[0],weight=float(new_data[1][1:])).last()
            if current:
                InfoFields.objects.create(
                    username_id=1,
                    number=new_data[0],
                    weight=float(new_data[1][1:]),
                    age=current.age,
                    gender=current.gender,
                    feed=current.feed
                )
                send_string(send)
                print('ok')
            else:
                InfoFields.objects.create(
                    username_id=1,
                    number=new_data[0],
                    weight=float(new_data[1][1:])
                )
                send_string(send)
                print('ok')
    except:
        print(traceback.format_exc())
