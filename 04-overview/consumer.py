import json
from config import channel
from constants import logs_queues


def on_receive_msg(ch, method, properties, body):
    payload = json.loads(body.decode())
    print(f"{payload['severity']}:{payload['msg']}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.exchange_declare(exchange="logs", exchange_type="direct", durable=True)

for queue in logs_queues:
    channel.queue_declare(queue=queue["queue"], durable=True)
    channel.queue_bind(queue=queue["queue"], routing_key=queue["bind"], exchange="logs")

for queue in logs_queues:
    channel.basic_consume(queue=queue["queue"], on_message_callback=on_receive_msg)

print("Starting Consuming Queues...")
channel.start_consuming()
