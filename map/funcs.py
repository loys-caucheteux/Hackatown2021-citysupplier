from geopy.geocoders import Nominatim

def getlat_fadress(adress):
    geoloc = Nominatim(user_agent="map")
    location = geoloc.geocode(adress)
    try:
        return location.latitude
    except AttributeError:
        return 1084


def getlon_fadress(adress):
    geoloc = Nominatim(user_agent="map")
    location = geoloc.geocode(adress)
    try:
        return location.longitude
    except AttributeError:
        return 1084