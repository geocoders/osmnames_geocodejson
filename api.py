# encoding: utf-8

from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import os

app = Flask(__name__)
api = Api(app)

OSMNAMES_API_BASE_URL = 'https://geocoder.tilehosting.com/q/{}.js'
OSMNAMES_API_KEY = os.environ.get('OSMNAMES_API_KEY')
if not OSMNAMES_API_KEY:
    raise Exception('OSMNAMES_API_KEY environment var is not set.')

def point_to_geocodejson(a_place):
    feature = {"type" : "Feature"}
    feature['geometry'] = {"type" : "Point", "coordinates" : [float(a_place['lon']), float(a_place['lat'])]}
    feature['properties'] = {}
    feature['properties']["type"] = a_place['type']
    feature['properties']["id"] = a_place['id']
    feature['properties']["name"] = a_place['name']
    feature['properties']["street"] = a_place['street']
    feature['properties']["label"] = a_place['display_name']
    feature['properties']["city"] = a_place['city']
    feature['properties']["country"] = a_place['country']
    feature['properties']["housenumber"] = a_place['housenumbers']
    feature['properties']["osm_key"] = a_place['class']
    feature['properties']["osm_value"] = a_place['type']

    return feature

class OSMNamesAutocomplete(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, help='the q you are you looking for', required=True)
        args = parser.parse_args()
        query = args['q']


        url = OSMNAMES_API_BASE_URL.format(query)
        params = {
            'key': OSMNAMES_API_KEY,
        }

        get_search = requests.get(url, params = params)

        initial_places = get_search.json()["results"]
        features = []

        for a_place in initial_places :
            a_feature = point_to_geocodejson(a_place)
            features.append(a_feature)

        geocoder_json = {
            "type" : "FeatureCollection",
            "query" : query,
            "features" : features,
            "_initial_response" : initial_places
        }

        return geocoder_json

api.add_resource(OSMNamesAutocomplete, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
