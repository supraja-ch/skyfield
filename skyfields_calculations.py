from flask import Flask, request
import flask
from flask import jsonify
from flask_cors import CORS, cross_origin

# skyfileds
from skyfield.api import load
from skyfield.api import Topos, EarthSatellite
import json

app = Flask(__name__)
CORS(app, support_credentials=True)

#  0 SOLAR SYSTEM BARYCENTER, 1 MERCURY BARYCENTER, 2 VENUS BARYCENTER, 3 EARTH BARYCENTER, 4 MARS BARYCENTER, 5 JUPITER BARYCENTER, 
#  6 SATURN BARYCENTER, 7 URANUS BARYCENTER, 8 NEPTUNE BARYCENTER, 9 PLUTO BARYCENTER, 10 SUN, 199 MERCURY, 399 EARTH, 299 VENUS, 
#  301 MOON, 499 MARS

@app.route('/distance_planets', methods=['GET'])
def distance_planets():
# position of Mars in the sky is as easy as:
    planets = load('de421.bsp')
    earth, mars,moon = planets['earth'], planets['mars'],  planets['moon']

    ts = load.timescale()
    t = ts.now()
    astrometric = earth.at(t).observe(moon)
    ra, dec, distance = astrometric.radec()
    # print(mars)
    # print(ra)
    # print(dec)
    # print(distance)     #finding the distance of moon to earth
    response = []
    details = {"ra":str(ra),"dec":str(dec),"distance":str(distance.AU*149597870)}
    response.append(details)
    return jsonify(response)

# print(mars)
# print(ra)
# print(dec)
# print(distance) finding the distance of moon to earth
# print(distance.AU * 149597870) #calculating the au to km
# --------------------------------------------------------------------

@app.route('/lcn_Earths_surface', methods=['GET'])
def lcn_Earths_surface():
    # specific to your location on the Earth’s surface:
    planets = load('de421.bsp')
    earth,mars = planets['earth'], planets['mars']
    boston = earth + Topos('17.9689 N', '79.5941 E') #warangla long abd lati
    ts = load.timescale()
    t = ts.now()
    astrometric = boston.at(t).observe(mars)
    alt, az, distance = astrometric.apparent().altaz()
    response = []
    details = {"ra":str(alt),"dec":str(az),"distance":str(distance.AU*149597870)}
    response.append(details)
    return jsonify(response)
# print(astrometric,"astrometric")
# print(alt,"altttttt")
# print(az,"azzzzzzzzzzzz")
# --------------------------------------------------------------------

@app.route('/finding_satellite_ele', methods=['GET'])
def finding_satellite_ele():
    # Finding and loading satellite elements:

    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'  
    # last_30_days = 'http://celestrak.com/NORAD/elements/tle-new.txt'
    # satellites = load.tle_file(last_30_days)
    satellites = load.tle_file(stations_url)
    # # print('Loaded', len(satellites), 'satellites')
    by_name = {sat.name: sat for sat in satellites}
    # satellite = by_name['ISS (ZARYA)']
    # # print(satellite)
    planets = load('de421.bsp')
    #finding sunligth in earth from mars
    earth, venus = planets['earth'], planets['moon']
    satellite = by_name['ISS (ZARYA)']
    ts = load.timescale()
    two_hours = ts.utc(2019, 8, 14, 0, range(0, 120, 20))
    p = (earth + satellite).at(two_hours).observe(venus).apparent()
    # print(p)
    sunlit = p.is_behind_earth()
    sunlight = []
    for t_h, sunlit_i in zip(two_hours, sunlit):
        data = '{}  {} is in {}'.format(
            t_h.utc_strftime('%Y-%m-%d %H:%M'),
            satellite.name,
            'sunlight' if sunlit_i else 'shadow')
        sunlight.append(data)
    
    bluffton = Topos('20.5937 N', '78.9629 E', elevation_m=43)
    t0 = ts.utc(2020, 8, 13)
    t1 = ts.utc(2020, 8, 14)
    tn, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=30.0)
    sunlight_time = []
    for ti, event in zip(tn, events):
        name = ('rise above 30°', 'culminate', 'set below 30°')[event]
        time = ti.utc_strftime('%Y %b %d %H:%M:%S'), name
        sunlight_time.append(time)
    return jsonify({"earth_light":sunlight,"sunlight_time":sunlight_time})

# without loading file 
# ts = load.timescale()
# line1 = '1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082'
# line2 = '2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473'
# satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
# print(satellite)
# print(satellite.epoch.utc_jpl()) #print human readable format

# finding when a satellite rises and sets

# bluffton = Topos('40.8939 N', '83.8917 W')

# print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

@app.route('/distance_planets_earth', methods=['GET'])
def distance_planets_earth():
# distance diff planets from earth
    ts = load.timescale()
    t = ts.now()
    planets = load('de421.bsp')
    v = planets['SUN'].at(t) - planets['earth'].at(t)
    distance  =  v.distance().km
    return jsonify({"distace":distance})
     

if __name__ == '__main__':
    app.run(host='127.0.0.1',port ='5000',debug=True)