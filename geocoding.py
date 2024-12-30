import requests

# La tua chiave API di Google
API_KEY = "AIzaSyAwUffePIA3gL_Cz2qadHa6v-RFg9MWIZc"

def geocode_address(address):
    """
    Converte un indirizzo in coordinate geografiche utilizzando l'API Geocoding di Google Maps.
    :param address: L'indirizzo da geocodificare
    :return: Una tuple (latitudine, longitudine) o None se non trova il risultato
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK":
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Errore: {data['status']}")
            return None
    else:
        print(f"Errore HTTP: {response.status_code}")
        return None
        