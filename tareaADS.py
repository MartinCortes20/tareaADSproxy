import requests
import json
import os

# Clase Servicio que hace la consulta a la PokeAPI
class Servicio:
    def get_pokemon_data(self, pokemon_name):
        print(f"[API] Obteniendo datos de {pokemon_name} desde la PokeAPI")
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] No se encontró el Pokémon {pokemon_name}")
            return None

# Clase Proxy que almacena los Pokémon localmente en un archivo JSON
class Proxy:
    def __init__(self, servicio, cache_file='pokemon_cache.json'):
        self.servicio = servicio
        self.cache_file = cache_file
        self.cache = self._load_cache()

    # Cargar el caché desde el archivo JSON
    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                print("[CACHÉ] Cargando datos del archivo cache")
                return json.load(file)
        return {}

    # Guardar el caché en el archivo JSON
    def _save_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file, indent=4)
        print("[CACHÉ] Guardando datos en el archivo cache")

    def get_pokemon_data(self, pokemon_name):
        # Si el Pokémon está en el caché, lo devolvemos
        if pokemon_name in self.cache:
            print(f"[CACHÉ] Pokémon {pokemon_name} encontrado en caché")
            return self.cache[pokemon_name]
        
        # Si no está, se usar el servicio para obtenerlo de la API
        data = self.servicio.get_pokemon_data(pokemon_name)
        if data:
            print(f"[CACHÉ] Guardando {pokemon_name} en caché")
            self.cache[pokemon_name] = data
            self._save_cache()  # Guarda datos en el archivo JSON
        return data

# Clase Cliente que interactúa con el Proxy
class Cliente:
    def __init__(self, servicio_proxy):
        self.servicio_proxy = servicio_proxy

    def solicitar_pokemon(self, pokemon_name):
        data = self.servicio_proxy.get_pokemon_data(pokemon_name)
        if data:
            print(f"Nombre: {data['name']}, Altura: {data['height']}, Peso: {data['weight']}")
        else:
            print("Pokémon no encontrado.")

# Inicializamos el servicio y el proxy
servicio = Servicio()
proxy = Proxy(servicio)
cliente = Cliente(proxy)

# Bucle para seguir preguntando
if __name__ == "__main__":
    while True:
        pokemon = input("Introduce el nombre de un Pokémon (o escribe 'Nos vemos' para terminar): ")
        
        # Condición para Nos vemos del bucle
        if pokemon.lower() == 'nos vemos':
            print("Saliendo del programa.")
            break
        
        cliente.solicitar_pokemon(pokemon)