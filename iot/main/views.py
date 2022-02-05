from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
# DHT11
import time
import board
import adafruit_dht
import psutil

def index(request):
    # We first check if a libgpiod process is running. If yes, we kill it!
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()

    sensor = adafruit_dht.DHT11(board.D23)
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        sensor.exit()
        raise error
    context = {
        'temp' : temp,
        'hum' : humidity,
    }
    return render(request, 'main/index.html', context)