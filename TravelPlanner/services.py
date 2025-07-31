import requests, os
from dotenv import load_dotenv

load_dotenv()

def getCoordinates(city):
    try:
        params = {
            'q': city,
            'format': 'json'
        }
        headers = {"User-Agent": "SmartTravelPlanner/1.0"}
        response = requests.get(os.getenv('OPENSTREETMAP_API_URL'), headers=headers, params=params)
        if(response.status_code != 200):
            return {}, response.status_code
        data=response.json()
        result = {
            'name': data[0].get('name'),
            'type': data[0].get('type'),
            'lat': data[0].get('lat'),
            'lon': data[0].get('lon'),
            'address': data[0].get('display_name')
        }
        return result, response.status_code

    except Exception as e:
        return {"error": str(e)}, 404

def getWeatherCodeValue(code):
    weathercodes = {
            (0,): ["Clear sky", 1],
            (1, 2, 3): ["Partly Cloudy", 2],
            (66, 67): ["cloudy", 3],
            (51, 53, 55, 56, 57): ["Drizzle", 4],
            (61, 63, 65, 80, 81, 82): ["Rainy", 5],
            (95, 96, 99): ["Thunderstorm", 6],
            (45, 48): ["Fog", 7],
            (71, 73, 75, 77,85, 86): ["Snowy", 8]
        }
    for key, value in weathercodes.items():
        if code in key:
            return value
    return None

def getWeatherReport(lat, lon):
    try:
        params = {
            "latitude": lat,
	        "longitude": lon,
            "hourly": ["is_day"],
	        "daily": ["apparent_temperature_mean", "weather_code", "wind_speed_10m_max", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_mean", "rain_sum", "snowfall_sum"],
            'minutely_15': ['relative_humidity_2m', 'dew_point_2m', 'visibility'],
            'forecast_minutely_15': 1,
            'current_weather': True,
            'timezone': 'IST',
        }
        response = requests.get(os.getenv('OPENMETEO_API_URL'), params=params)
        if(response.status_code != 200):
            return {}, response.status_code
        data = response.json()
        current = data.get('current_weather', None)
        skyWeather = getWeatherCodeValue(current.get('weathercode'))
        if current:
            result = {
                'is_day': current.get('is_day'),
                'current_time': current.get('time')[-5:],
                'temperature': current.get('temperature'),
                'apparent_temperature': data['daily'].get('apparent_temperature_mean')[0],
                'wind': current.get('windspeed'),
                'weathercode': skyWeather,
                'temp_max': data['daily'].get('temperature_2m_max')[0],
                'temp_min': data['daily'].get('temperature_2m_min')[0],
                'precipitation': data['daily'].get('precipitation_probability_mean')[0],
                'rain': data['daily'].get('rain_sum')[0],
                'dew': data['minutely_15'].get('dew_point_2m')[0],
                'humidity': data['minutely_15'].get('relative_humidity_2m')[0],
                'snow': data['daily'].get('snowfall_sum')[0],
                'visibility': data['minutely_15'].get('visibility')[0] / 1000
            }
            return result, response.status_code

    except Exception as e:
        return {"error": str(e)}, 404
    
def getAttractions(lat, lon, radius):
    priority = [
        'hindu_temples', 'mosques', 'cathedrals', 'churches', 'museums', 'cinemas', 'zoos', 'waterfalls', 
        'beaches', 'rivers', 'dry_lakes', 'mountain_peaks', 'amusement_parks', 'gardens_and_parks',
        'stadiums', 'aquariums', 'art_galleries', 'monuments_and_memorials', 'castles', 'restaurants',
        'fast_food', 'bars', 'cafes', 'malls', 'supermarkets', 'foods', 'shops', 'religion', 'historic_architecture',
        'natural', 'cultural', 'historic'
    ]
    historic = ['historic_architecture', 'historic', 'museums', 'monuments_and_memorials', 'cultural', 'art_galleries', 'castles']
    nature = ['gardens_and_parks', 'natural', 'dry_lakes', 'waterfalls', 'rivers', 'beaches', 'mountain_peaks']
    religion = ['religion', 'hindu_temples', 'mosques', 'churches', 'cathedrals']
    entertainment = ['cinemas', 'amusement_parks', 'zoos', 'stadiums', 'aquariums']
    food = ['restaurants', 'foods', 'cafes', 'fast_food', 'bars']
    shop = ['shops', 'malls', 'supermarkets']

    historical_places = []
    natural_places = []
    religious_places = []
    entertainment_places = []
    food_places = []
    shopping_places = []
    others=[]
    try:
        places = []
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'kinds': 'historic_architecture,historic,museums,monuments_and_memorials,cultural,art_galleries,castles',
            'apikey': os.getenv('OPENTRIP_API_KEY')
        }
        response1 = requests.get(os.getenv('OPENTRIP_API_URL') + 'radius', params=params)
        if(response1.status_code != 200):
            return {}, response1.status_code
        places.extend(response1.json().get('features', []))
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'kinds': 'gardens_and_parks,natural,dry_lakes,waterfalls,rivers,beaches,mountain_peaks',
            'apikey': os.getenv('OPENTRIP_API_KEY')
        }
        response2 = requests.get(os.getenv('OPENTRIP_API_URL') + 'radius', params=params)
        if(response2.status_code != 200):
            return {}, response2.status_code
        places.extend(response2.json().get('features', []))
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'kinds': 'religion,hindu_temples,mosques,churches,cathedrals',
            'apikey': os.getenv('OPENTRIP_API_KEY')
        }
        response3 = requests.get(os.getenv('OPENTRIP_API_URL') + 'radius', params=params)
        if(response3.status_code != 200):
            return {}, response3.status_code
        places.extend(response3.json().get('features', []))
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'kinds': 'cinemas,amusement_parks,zoos,stadiums,aquariums',
            'apikey': os.getenv('OPENTRIP_API_KEY')
        }
        response4 = requests.get(os.getenv('OPENTRIP_API_URL') + 'radius', params=params)
        if(response4.status_code != 200):
            return {}, response4.status_code
        places.extend(response4.json().get('features', []))
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'kinds': 'restaurants,foods,cafes,fast_food,bars,shops,malls,supermarkets',
            'apikey': os.getenv('OPENTRIP_API_KEY')
        }
        response5 = requests.get(os.getenv('OPENTRIP_API_URL') + 'radius', params=params)
        if(response5.status_code != 200):
            return {}, response5.status_code
        places.extend(response5.json().get('features', []))

        if not places:
            return {'error': 'no data available'}

        seen_names = set()

        for place in places:
            properties = place.get('properties', {})
            name = properties.get('name', '').strip()
            kinds = properties.get('kinds', '')

            if not name or name.lower() in seen_names:
                continue
            seen_names.add(name.lower())

            if kinds:
                kinds_list = kinds.split(',')

                assigned = False
                for kind in priority:
                    if kind in kinds_list:
                        if kind in historic:
                            properties['category'] = kind.replace('_', ' ')
                            historical_places.append(place)
                        elif kind in nature:
                            properties['category'] = kind.replace('_', ' ')
                            natural_places.append(place)
                        elif kind in religion:
                            properties['category'] = kind.replace('_', ' ')
                            religious_places.append(place)
                        elif kind in entertainment:
                            properties['category'] = kind.replace('_', ' ')
                            entertainment_places.append(place)
                        elif kind in food:
                            properties['category'] = kind.replace('_', ' ')
                            food_places.append(place)
                        elif kind in shop:
                            properties['category'] = kind.replace('_', ' ')
                            shopping_places.append(place)
                        else:
                            properties['category'] = kind.replace('_', ' ')
                            others.append(place)
                        assigned = True
                        break 
                if not assigned:
                    properties['category'] = kind.replace('_', ' ')
                    others.append(place)

        historical_places = sorted(
            historical_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        natural_places = sorted(
            natural_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        religious_places = sorted(
            religious_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        entertainment_places = sorted(
            entertainment_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        food_places = sorted(
            food_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        shopping_places = sorted(
            shopping_places,
            key=lambda x: x['properties'].get('rate', 0),
            reverse=True
        )
        
        result = {
            'historical_places': [],
            'natural_places': [],
            'religious_places': [],
            'entertainment_places': [],
            'food_places': [],
            'shopping_places': []
        }

        for place in historical_places[0:8]:
            result['historical_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        
        for place in natural_places[0:8]:
            result['natural_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in religious_places[0:8]:
            result['religious_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in entertainment_places[0:8]:
            result['entertainment_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in food_places[0:8]:
            result['food_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })

        for place in shopping_places[0:8]:
            result['shopping_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['rate'],
                    })
        
        return result, 200

    except Exception as e :
        return {'error': str(e)}, 404
