import serial
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_scale.settings')
django.setup()
from django.utils import timezone
import traceback
send = serial.Serial('COM22',19200,timeout=1)
print("Connect success", send)

def send_string(strings):
    try:
        return send.write(strings)
    except Exception:
        print("I can't connection {err}".format(EnvironmentError))