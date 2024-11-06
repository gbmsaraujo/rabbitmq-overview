import json
from rabbitmq_config import channel
import time

import json
from rabbitmq_config import channel
import time

routings = [
    {"queue": "critical_logs_queue", "routing": "critical_logs"},
    {"queue": "general_logs_queue", "routing": "general_logs"},
]


def callback(ch, method, properties, body):
    print(f"Message Received: {method.routing_key} - {body.decode()}")
    print("Done!")


# Declarar a exchange
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

# Declarar e vincular filas
for routing in routings:
    channel.queue_declare(
        queue=routing["queue"], durable=True
    )  # Remova exclusive=True se quiser persistência
    channel.queue_bind(
        exchange="direct_logs", queue=routing["queue"], routing_key=routing["routing"]
    )

# Consumir de cada fila
for routing in routings:
    channel.basic_consume(
        queue=routing["queue"], on_message_callback=callback, auto_ack=True
    )

print("Starting consuming....")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    channel.close()  # Certifique-se de fechar o canal adequadamente
