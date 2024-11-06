from rabbitmq_config import channel, connection_rmq

channel.queue_declare(queue="letterbox")

message = "Hello, this is my first message"

channel.basic_publish(exchange="", routing_key="letterbox", body=message)

print(f"Sent message: {message}")

connection_rmq.close()

