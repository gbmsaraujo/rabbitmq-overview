import json
from rabbitmq_config import channel
import time


def callback(ch, method, properties, body):
    msg = json.loads(body.decode())
    print(f" Message Received: {msg['text']}")
    time.sleep(msg["time"])
    # Garante manualmente que se o worker encerrar por algum motivo ao longo de um processo, ele não descartará o processo
    # que estava sendo executado, e executará novamente
    # a task vai esperar que o processamento seja concluído.
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Done!")


channel.queue_declare(queue="hello")


# Garante que um consumer receba uma task só quando finalizar o tratamento da anterior;
# Isso evita gargalos na fila e sobrecargas;
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="hello", on_message_callback=callback)

print("Starting consuming....")

channel.start_consuming()
