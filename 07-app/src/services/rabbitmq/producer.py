import json
import uuid
from src.configs.rabbitmq_config import RabbitMQConfig


class RpcClientProducer:

    def __init__(self, queue_name: str, exchange_name):

        self.queue_name = queue_name
        self.rmq_config = RabbitMQConfig()
        self.correlation_id = None
        self.response = None
        self.callback_queue = None
        self.exchange = exchange_name

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = body.decode()
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, payload: tuple, routing_name: str):
        print(
            f"Sending request to {routing_name} value={payload} with correlation_id {self.correlation_id}"
        )

        with self.rmq_config as channel:
            self.correlation_id = str(uuid.uuid4())
            temporary_queue = channel.queue_declare("", exclusive=True)
            temporary_queue_name = temporary_queue.method.queue
            self.callback_queue = temporary_queue_name

            channel.exchange_declare(self.exchange, exchange_type="direct")
            channel.queue_declare(queue=self.queue_name)
            channel.queue_bind(
                queue=self.queue_name, routing_key=routing_name, exchange=self.exchange
            )

            channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_name,
                properties=self.rmq_config.basic_properties(
                    correlation_id=self.correlation_id, reply_to=temporary_queue_name
                ),
                body=json.dumps(payload),
            )

            # Configura o consumidor para a fila de resposta
            self.rmq_config.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
            )

            while self.response is None:
                print("Waiting response...")
                self.rmq_config.connection.process_data_events(time_limit=None)
                

        return self.response
