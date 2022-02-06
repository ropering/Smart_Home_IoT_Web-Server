from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
    else:
        context = {
            'temp' : temp,
            'hum' : humidity,
        }
        return render(request, 'main/index.html', context)
    return HttpResponse('<h1>다시 실행해주세요</h1>')

def get_dht_data():
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    sensor = adafruit_dht.DHT11(board.D23)

    try:
        temp = sensor.temperature
        hum = sensor.humidity
        if temp is not None and hum is not None:
            return temp, hum
    except RuntimeError as err:
        print('1', err.args[0])
        return None, None
    except Exception as err:
        sensor.exit()
        raise ('2', err)

def get_value(request):
    temp, hum = get_dht_data()
    return JsonResponse({"temp": temp, "hum": hum})

def test(request):
    return JsonResponse({"text" : 'Hello world~'})