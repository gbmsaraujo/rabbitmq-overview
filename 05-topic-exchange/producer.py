import json
import pika
from config import channel, connection_rmq
from constants import logs_messages, logs_queues

try:

    channel.exchange_declare(exchange="topic_logs", exchange_type="topic", durable=True)

    for queue in logs_queues:
        channel.queue_declare(queue=queue["queue"], durable=True)

    for msg in logs_messages:
        channel.basic_publish(
            exchange="topic_logs",
            body=json.dumps(msg),
            routing_key=msg["severity"],
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

        print(f"Mensagem {msg['msg']} enviado com sucesso para fila!")

except ValueError as e:
    print(e)

finally:
    connection_rmq.close()
