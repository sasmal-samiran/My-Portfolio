from flask import Blueprint, request, jsonify, render_template, url_for
import TravelPlanner.services as services

travelplanner = Blueprint('travelplanner', 
    __name__, 
    template_folder='templates', 
    static_folder='static',  
    url_prefix='/travelplanner')

@travelplanner.route('/')
def home():
    return render_template('home.html')

@travelplanner.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@travelplanner.route('/travelplanner', methods=["POST"])
def weatherReport():
    data = request.get_json()
    city = data.get('city')
    radius = data.get('radius')
    if city == '':
        coordinates = {
            'name': "Your Location" if (data.get('currentLat') != 28.6139) else 'New Delhi',
            'type': '',
            'lat': data.get('currentLat'),
            'lon': data.get('currentLon'),
            'address': ''
        }
    else:
        coordinates, status_code = services.getCoordinates(city)
    weatherReport, status_code = services.getWeatherReport(coordinates['lat'], coordinates['lon'])
    attractions, status_code = services.getAttractions(coordinates['lat'], coordinates['lon'], radius)
    weatherReport.update(coordinates)
    weatherReport.update(attractions)
    return jsonify(weatherReport), status_code
        