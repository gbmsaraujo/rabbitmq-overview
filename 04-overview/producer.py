import json
import pika
from config import channel, connection
from constants import ROUTING_LOG_KEY, logs_messages, logs_queues

channel.exchange_declare(exchange="logs", exchange_type="direct", durable=True)


def set_routing_key(severity: str):
    return "critical_log_bind" if severity == "critical" else "general_log_bind"


for queue in logs_queues:
    channel.queue_declare(queue=queue["queue"], durable=True)

for msg in logs_messages:
    channel.basic_publish(
        exchange="logs",
        body=json.dumps(msg),
        routing_key=set_routing_key(msg["severity"]),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )

    print(f"Mensagem {msg['msg']} enviado com sucesso para fila!")
