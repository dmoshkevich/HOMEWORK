import requests
import json
from flask import Flask
from flask import request
import configparser  # импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")

app = Flask(__name__)


def get_lat_lon(city_name):
    open_cage_url = (config["Opencage"]["url"] + city_name + config["Opencage"]["api_key"])
    response = requests.request("GET", open_cage_url)
    res = response.json()
    lat = res['results'][1]['bounds']['southwest']['lat']
    lon = res['results'][1]['bounds']['southwest']['lng']
    return lat, lon


def get_weather_json(city_name, req_type):
    lat, lon = get_lat_lon(city_name)
    url = config["Weatherbit"]["url"] + req_type
    querystring = {"lang": "en", "lat": lat, "lon": lon}
    headers = {
        'x-rapidapi-host': config["Weatherbit"]["api_host"],
        'x-rapidapi-key': config["Weatherbit"]["api_key"]
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


@app.route('/v1/forecast/')
def get_forecast():
    city_name = request.args.get('city')
    res = get_weather_json(city_name, 'forecast/daily')
    timestamp = request.args.get('dt')

    if timestamp:
        timestamp = '2020-' + timestamp[0:2] + '-' + timestamp[2:4]
        for i in res['data']:
            if timestamp == str(i['valid_date']):
                return '{ "city":' + city_name + ' ,"unit": "celsius" ,"temperature":' + str(i['temp']) + '}'
    return 'not fount ((((('


@app.route('/v1/current/')
def get_current():
    city_name = request.args.get('city')
    res = get_weather_json(city_name, 'current')
    return '{ "city": ' + city_name + ' ,"unit": "celsius", "temperature": ' + str(res['data'][0]['app_temp']) + '}'


if __name__ == '__main__':
    app.run(debug=True)
