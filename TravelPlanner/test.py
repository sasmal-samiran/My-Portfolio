import requests, os
from dotenv import load_dotenv

load_dotenv()

import requests

# overpass_url = "https://overpass-api.de/api/interpreter"
# query = """
# [out:json];
# node(around:5000,22.8400,88.6630)[tourism];
# out;
# """

# response = requests.post(overpass_url, data={'data': query})
# data = response.json()

# # Extract POIs
# pois = []
# for element in data['elements']:
#     name = element['tags'].get('name', 'Unknown')
#     category = element['tags'].get('tourism', 'N/A')
#     lat = element['lat']
#     lon = element['lon']
#     print(name)
#     pois.append({
#         # 'name': name,
#         # 'category': category,
#         # 'lat': lat,
#         # 'lon': lon
#     })

# print(data['elements'][0])
# print(type(data['elements'][0]))
# print(len(data['elements']))

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

        for place in historical_places[0:10]:
            result['historical_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        
        for place in natural_places[0:10]:
            result['natural_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in religious_places[0:10]:
            result['religious_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in entertainment_places[0:10]:
            result['entertainment_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })
        for place in food_places[0:10]:
            result['food_places'].append({
                        'lat': place['geometry']['coordinates'][1],
                        'lon': place['geometry']['coordinates'][0],
                        'xid': place['properties']['xid'],
                        'name': place['properties']['name'],
                        'distance': round(place['properties']['dist'] / 1000, 2),
                        'category': place['properties']['category'],
                    })

        for place in shopping_places[0:10]:
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
