import json
from src.configs.rabbitmq_config import RabbitMQConfig


class RPCClientConsumer:
    def __init__(self, queue_name: str, exchange_name):
        self.queue = queue_name
        self.exchange = exchange_name
        self.rmq_config = RabbitMQConfig()
        self.action = None

    def __on_request(self, ch, method, props, body):
        payload, description = json.loads(body)
        print(f"{description}")

        response = self.action(payload)

        print(
            f"Sending response to {props.reply_to} with correlation_id {props.correlation_id}"
        )
    

        with self.rmq_config as channel:

            channel.basic_publish(
                exchange="",
                routing_key=props.reply_to,
                properties=self.rmq_config.basic_properties(
                    reply_to=props.reply_to, correlation_id=props.correlation_id
                ),
                body=json.dumps(response),
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self, routing_key: str, action):
        with self.rmq_config as channel:
            self.action = action
            channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
            channel.queue_declare(queue=self.queue)
            channel.queue_bind(
                queue=self.queue, routing_key=routing_key, exchange=self.exchange
            )
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=self.queue, on_message_callback=self.__on_request
            )
            print(f"Aguardando requisições na fila {self.queue}")
            channel.start_consuming()
