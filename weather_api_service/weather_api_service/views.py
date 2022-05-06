
import sys
import json
#import jwt
import datetime
from flask_restful import Resource,Api,reqparse
from flask import Flask,request,render_template,make_response
from flask_jwt_extended import jwt_required, get_jwt_identity,JWTManager
from flask_jwt_extended import create_access_token
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from config import *
from utils import *
import HttpResponse
import jsonify
#from api_class import Weather,List_countries,List_cities
import User_model
import User_services as user_service 
from weather_api_service import db,api,app,secret_key
from flask import Flask, g


from flask import Flask, g
from flask_track_usage import TrackUsage
from flask_track_usage.storage.printer import PrintWriter
from flask_track_usage.storage.output import OutputWriter

#tracking usage 
t = TrackUsage(app, [
		PrintWriter(),
		OutputWriter(transform=lambda s: "OUTPUT: " + str(s))
        ])


with open(r"./data/country_data.json",encoding="utf8") as infile:
    location_data = json.loads(infile.read())
               
def get_countrylist():
    country =[]
    for val in location_data:
        if val["country"] not in country:
            country.append(val["country"])
    return country 
    
    

def get_city(country):
    city =[]
    for val in location_data:
        if val["country"] == country:
            if val["name"] not in city:
                city.append(val["name"])
    return city
    
def get_weather(city,days=1):
    if days == 1:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url).json()
        loc_name = response["location"]["name"]
        loc_region = response["location"]["region"]
        curr_temp_c = response["current"]["temp_c"]
        curr_condition = response["current"]["condition"]["text"]
        feels_like = response["current"]["feelslike_c"]
        return loc_name,loc_region,curr_temp_c,curr_condition,feels_like
    else:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days={days}&aqi=no&alerts=no"
        response = requests.get(url).json()
        loc_name = response["location"]["name"]
        loc_region = response["location"]["region"]
        curr_temp_c = response["current"]["temp_c"]
        curr_condition = response["current"]["condition"]["text"]
        feels_like = response["current"]["feelslike_c"]
        forecast = response["forecast"]["forecastday"]
        return loc_name,loc_region,curr_temp_c,curr_condition,feels_like,forecast
        #return response
    

#api.add_resource(Weather,"/city/<string:city>")
#api.add_resource(List_countries,"/country/list")
#api.add_resource(List_cities,"/city/list/<string:country>")  


@app.route('/login', methods=['POST'])
def login():
    try:
        #payload: dict = request.json
        user_name: str = request.args.get('user_name', None)
        password: str = request.args.get('password', None)
        if user_name and password:
            status, message, data = user_service.validate_user_credentials(user_name=user_name, password=password)
            if status == 200:
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(data), expires_delta=expires)
                #access_token = jwt.encode(payload=data, key=secret_key)
                data['access_token'] = access_token
                app.logger.info(f"logged_user_name :{user_name}") 
        else:
            status, message, data = (400, 'Bad request', None)

        response = HttpResponse.HttpResponse(message=message, status=status, data=data)
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse.HttpResponse(message='Exception Occured - '+exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())
    
   
@app.route('/weatherapp', methods=['POST'])   
@jwt_required()
def weatherapp():
    #if request.method == 'GET' and request.form.get('country', None):
        #country: str = request.form.get('country', None)
        #return render_template("index.html",countrylist = get_countrylist(),citylist = get_city(country))
    if request.args.get('city', None):
        city: str = request.args.get('city', None)
        loc_name,loc_region,curr_temp_c,curr_condition,feels_like = get_weather(city)
        return {"location name":loc_name,"region":loc_region,"current temperature":curr_temp_c,"condition":curr_condition,"feels like":feels_like}
    else:
        return "invalid inputs"


@app.route('/forecast', methods=['POST'])

@jwt_required()
def forecast():
    #app.logger.info(f"request_obj :{request}") 
    #app.logger.info(f"request_by :{get_jwt_identity()}") 
    if request.args.get('city', None) and request.args.get('days'):
        city = request.args.get('city', None)
        days = request.args.get('days', None)
        loc_name,loc_region,curr_temp_c,curr_condition,feels_like,forecast =get_weather(city,days)
        return {"location name":loc_name,"region":loc_region,"current temperature":curr_temp_c,"condition":curr_condition,"feels like":feels_like,"forecast":forecast}
    else:
        return {"invalid inputs":"Please enter city and no of days to forecast"}


@app.route('/countrylist', methods=['GET'])
@jwt_required()
def countrylist():
    return {"country":get_countrylist()}


@app.route('/citylist', methods=['POST'])
@jwt_required()
def citylist():

    if request.args.get('country', None):
        country = request.args.get('country', None)
        return {"cities":get_city(country)}
        
@t.include
@app.route('/track')       
def track_api():
    g.track_var["optional"] = "Hello"
    return t

jwt = JWTManager(app)  

     

    
    
    

