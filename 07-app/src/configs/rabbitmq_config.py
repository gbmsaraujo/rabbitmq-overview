import pika


class RabbitMQConfig:
    def __init__(self, host="localhost", username="guest", password="guest") -> None:
        self.__user_credentials = pika.PlainCredentials(username, password)
        self.__host = host

        self.connection = None
        self.channel = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.__host, credentials=self.__user_credentials
            )
        )
        self.channel = self.connection.channel()

        return self.channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    def basic_properties(self, reply_to: str, correlation_id: str):
        return pika.BasicProperties(reply_to=reply_to, correlation_id=correlation_id)
