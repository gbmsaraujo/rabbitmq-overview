from src.configs.rabbitmq_config import RabbitMQConfig
from src.controller.pokemon import PokeAPI
from src.services.rabbitmq.consumer import RPCClientConsumer
from src.services.rabbitmq.producer import RpcClientProducer


rmq = RabbitMQConfig()

class PokemonServiceProducer:
    def __init__(self) -> None:
        self.controller = PokeAPI()
        self.producer = RpcClientProducer("pokemon_queue", "pokemon_exchange")

    def send_pokemons_to_get_ability(self):
        pokemons = self.controller.get_pokemons()
        payload = (pokemons, "get abilities")
        response = self.producer.call(payload, "get_abilities")
        return response


class PokemonServiceConsumer:
    def __init__(self) -> None:
        self.controller = PokeAPI()
        self.consumer = RPCClientConsumer("pokemon_queue", "pokemon_exchange")

    def get_abilities_and_pokemons(self):
        self.consumer.start_consuming(
            "get_abilities", self.controller.get_pokemon_and_abilities
        )
