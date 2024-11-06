import requests


class PokeAPI:
    def get_pokemons(self):
        result = requests.get("https://pokeapi.co/api/v2/pokemon?limit=50")
        return [pokemon["name"] for pokemon in result.json()["results"]]

    def get_pokemon_and_abilities(self, pokemons):
        result = [
            {"pokemon": pokemon, "abilities": self.__get_abilities(pokemon)}
            for pokemon in pokemons
        ]

        return result

    def __get_abilities(self, pokemon: str):
        result = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")
        return [ability["ability"]["name"] for ability in result.json()["abilities"]]
