import pika
import json
import math
from config import RabbitMQConfig
from consts import EXCHANGE_NAME, EXCHANGE_TYPE

def calculate_factorial(n):
    return math.factorial(n)


def on_request(ch, method, props, body):
    n = int(body)
    print(f" [.] Calculating factorial({n})")
    # Envia a resposta para a fila reply_to com o mesmo correlation_id

    response = calculate_factorial(n)

    print(
        f"Sending response to {props.reply_to} with correlation_id {props.correlation_id}"
    )

    rmq.channel.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=rmq.basic_properties(
            reply_to=props.reply_to, correlation_id=props.correlation_id
        ),
        body=json.dumps(response),
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


rmq = RabbitMQConfig()

queue_name = "rpc_queue"
queue_bind = "rpc_queue_bind"

# rmq.channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)
rmq.channel.queue_declare(queue=queue_name)
# rmq.channel.queue_bind(queue=queue_name, routing_key=queue_bind, exchange=EXCHANGE_NAME)

rmq.channel.basic_qos(prefetch_count=1)
rmq.channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")

rmq.channel.start_consuming()
