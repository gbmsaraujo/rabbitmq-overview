import json
import pika
import uuid
from config import RabbitMQConfig
from consts import EXCHANGE_NAME, EXCHANGE_TYPE


class RpcClientProducer:

    def __init__(
        self,
        exchange_name: str = EXCHANGE_NAME,
        exchange_type: str = EXCHANGE_TYPE,
        routing_key: str = "",
    ):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key

        self.rmq = RabbitMQConfig()

        self.rmq.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type
        )
        # fila temporaria

        self.temporary_queue = self.rmq.channel.queue_declare(queue="", exclusive=True)
        self.correlation_id = str(uuid.uuid4())
        self.queue_name = self.temporary_queue.method.queue

        self.rmq.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.on_response, auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, payload: dict):
        print(
            f"Sending request to realize fatorial operation value={payload} with correlation_id {self.correlation_id}"
        )

        self.rmq.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            properties=self.rmq.basic_properties(
                correlation_id=self.correlation_id, reply_to=self.queue_name
            ),
            body=json.dumps(payload),
        )

        while self.response is None:
            print("Waiting response...")
            self.rmq.connection.process_data_events(time_limit=None)

        return json.loads(self.response)


