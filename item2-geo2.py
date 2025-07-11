import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "b2a3cfdb-df8f-4fa4-9432-a9b47a92ba2f"  # Reemplaza con tu propia API key si es necesario

def geocoding(location, key):
    while location.strip() == "":
        location = input("Ingresa la localización otra vez: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {state}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        print(f"Geocoding API URL para {new_loc} (Tipo de lugar: {value})\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de API Geocode: " + str(json_status) + "\nMensaje de error: " + json_data.get("message", "No hay mensaje disponible."))
    return json_status, lat, lng, new_loc

while True:
    print("\n==============================================")
    print("Perfiles de transporte disponibles en Graphhopper:")
    print("==============================================")
    print("car → automóvil")
    print("bike → bicicleta")
    print("foot → a pie")
    print("==============================================")
    print("Presiona 's' para salir en cualquier momento.")
    print("==============================================")

    profile = ["car", "bike", "foot"]
    vehicle = input("Elige un medio de transporte: ").lower()
    if vehicle in ["s", "q", "quit"]:
        break
    elif vehicle not in profile:
        print("Medio de transporte no válido. Se usará 'car' por defecto.")
        vehicle = "car"

    loc1 = input("Ciudad de origen: ")
    if loc1.lower() in ["s", "q", "quit"]:
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ciudad de destino: ")
    if loc2.lower() in ["s", "q", "quit"]:
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        response = requests.get(paths_url)
        paths_status = response.status_code
        paths_data = response.json()

        print("Estado de API de rutas: " + str(paths_status))
        print("URL de consulta:\n" + paths_url)
        print("=================================================")
        print("Ruta desde " + orig[3] + " hasta " + dest[3] + " usando " + vehicle)
        print("=================================================")

        if paths_status == 200:
            miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración estimada del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            print("Narrativa del viaje:")
            for step in paths_data["paths"][0]["instructions"]:
                path = step["text"]
                distance = step["distance"]
                print("- {0} ( {1:.1f} km / {2:.1f} millas )".format(path, distance/1000, distance/1000/1.61))
            print("=================================================")

            # Guardar resultado en archivo (opcional)
            with open("resultado_ruta.txt", "a") as file:
                file.write(f"Ruta desde {orig[3]} hasta {dest[3]} en {vehicle}\n")
                file.write(f"Distancia: {km:.1f} km / {miles:.1f} millas\n")
                file.write(f"Duración: {hr:02d}:{min:02d}:{sec:02d}\n")
                file.write("-" * 40 + "\n")
        else:
            print("Mensaje de error: " + paths_data.get("message", "No hay mensaje disponible."))
            print("*************************************************")
    else:
        print("Una de las solicitudes de geocodificación falló.")
        print("*************************************************")

print("\nGracias por usar el sistema de rutas. ¡Hasta pronto!")
