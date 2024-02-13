from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
import datetime

def index(request):
    appid = '24b19ca5abadf92f9399e321f383b650'
    URL = 'https://api.openweathermap.org/data/2.5/weather'
    PARAMS = {'q': 'Mymensingh', 'appid': appid, 'units': 'metric'}
    
    r = requests.get(url=URL, params=PARAMS)
    res = r.json()

    description = res['weather'][0]['description']
    icon = res['weather'][0]['icon']  
    temp = res['main']['temp']
    day = datetime.date.today()
    
    return render(request, 'index.html', {'description': description, 'icon': icon, 'temp': temp, 'day': day})

def search_weather(request):
    city_name = request.GET.get('city')  
    if city_name: 
        appid = '24b19ca5abadf92f9399e321f383b650'
        URL = 'https://api.openweathermap.org/data/2.5/weather'
        PARAMS = {'q': city_name, 'appid': appid, 'units': 'metric'}

        r = requests.get(url=URL, params=PARAMS)
        res = r.json()

        description = res['weather'][0]['description']
        icon = res['weather'][0]['icon']
        temp = res['main']['temp']
        day = datetime.date.today()

     
        return render(request, 'index.html', {'weather_info': {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'city': city_name}})
    else:
       
        return redirect('index')
    
    
    
    


def plan_optimal_routes():
    station_from = request.args.get('from')
    station_to = request.args.get('to')
    optimize = request.args.get('optimize')

    if not all([station_from, station_to, optimize]):
        
        return jsonify({"message": "Incomplete route information provided"}), 400

    if station_from not in stations or station_to not in stations:
        
        return jsonify({"message": "One or both stations not found"}), 404

    if optimize not in ['cost', 'time']:
        
        
        return jsonify({"message": "Invalid optimization parameter"}), 400
    
    

   
    if optimize == 'cost':



        optimalRoute = calculate_optimal_route_by_cost(station_from, station_to)
        
    else:

        optimalRoute = calculate_optimal_route_by_time(station_from, station_to) 

    if optimalRoute is None:
        
        return jsonify({"message": f"No routes available from station: {station_from} to station: {station_to}"}), 403


    response_route = []
    
    for i, station_id in enumerate(optimalRoute):
        station = stations[station_id]
        train_id = None
        arrival_time = None
        departure_time = None

        if i > 0:
            train_id = find_train_between_stations(optimalRoute[i-1], station_id)
            arrival_time = get_arrival_time(optimalRoute[i-1], station_id)
            departure_time = get_departure_time(optimalRoute[i-1], station_id)

        response_route.append({
            "station_id": station_id,
            "train_id": train_id,
            "arrival_time": arrival_time,
            "departure_time": departure_time
        })

    TotalCost = calculate_total_cost(optimalRoute)
    TotalTime = calculate_total_time(optimalRoute)

    response = {
        
        "TotalCost": TotalCost,
        "TotalTime": TotalTime,
        "stations": response_route
    }

    return jsonify(response), 200

