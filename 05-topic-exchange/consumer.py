import json
from config import channel
from constants import logs_queues

import json
from config import channel, connection_rmq
from constants import logs_queues


def on_receive_msg(ch, method, properties, body):
    payload = json.loads(body.decode())
    print(f"{method.routing_key} - {payload['severity']}:{payload['msg']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic", durable=True)

    for queue in logs_queues:
        channel.queue_declare(queue=queue["queue"], durable=True)
        channel.queue_bind(
            queue=queue["queue"], routing_key=queue["bind"], exchange="topic_logs"
        )

    for queue in logs_queues:
        channel.basic_consume(queue=queue["queue"], on_message_callback=on_receive_msg)

    print("Starting Consuming Queues...")
    channel.start_consuming()

except Exception as e:
    print(f"Erro: {e}")
finally:
    connection_rmq.close()
