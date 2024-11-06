import json
import pika
from rabbitmq_config import channel

# Durable mantem as mensagens na fila mesmo se o Rabbit Reiniciar;

result = channel.queue_declare(queue="", durable=True)
channel.queue_bind(exchange="logs", queue=result.method.)
