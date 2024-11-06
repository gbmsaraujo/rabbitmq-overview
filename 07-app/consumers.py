from src.services.pokemon.pokemon_service import PokemonServiceConsumer


pokemon_service = PokemonServiceConsumer()

pokemon_service.get_abilities_and_pokemons()
