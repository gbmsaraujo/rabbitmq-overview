import pika
from rabbitmq_config import channel

def on_message_received(ch, method, properties, body):
    print(f"received new message: {body}")


channel.queue_declare(queue="letterbox")

channel.basic_consume(
    queue="letterbox", auto_ack=True, on_message_callback=on_message_received
)

print("Starting consuming....")

channel.start_consuming()