from src.services.pokemon.pokemon_service import  PokemonServiceProducer


pokemon_service = PokemonServiceProducer()

response = pokemon_service.send_pokemons_to_get_ability()

print(response)
