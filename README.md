# OSMNames geocoder in geocodejson format

Run queries against [OSMNames geocoder](http://osmnames.org/api/) API with support of [geocodejson spec](https://github.com/geocoders/geocodejson-spec).

## Intalling

Python3 is needed.
To install the requirements :
```
    pipenv install
    pipenv shell
```

## Running

    OSMNAMES_API_KEY='your-osm_names_api_key' python api.py

Then, you can geocode some stuff :

        curl 'http://localhost:5000/?q=rue%20de%20la%20procession'

Or use [geocoder-tester](https://github.com/geocoders/geocoder-tester) :

        py.test --api-url http://localhost:5000/ --max-run 10
