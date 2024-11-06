import json
from config import RabbitMQConfig

class ClientOperationConsumer:
    def __init__(self, correlation_id, reply_to, rmq) -> None:
        self.__correlation_id = correlation_id
        self.__temporary_queue = reply_to
        self.response = None
        self.__rmq = rmq

        self.__rmq.channel.basic_consume(
            queue=self.__temporary_queue,
            on_message_callback=self.__on_response,
            auto_ack=True,
        )

    def __on_response(self, ch, method, props, body):
        if props.correlation_id == self.__correlation_id:
            print(f"print: {json.loads(body)}")
            self.response = json.loads(body)

    def wait_for_response(self):
        print(f" [x] Waiting for response with correlation ID {self.__correlation_id}")
        while self.response is None:
            self.__rmq.connection.process_data_events()
        print(f" [.] Got response: {self.response}")
