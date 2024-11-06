import pika


class RabbitMQConfig:
    def __init__(self, host="localhost", username="guest", password="guest") -> None:
        self.__user_credentials = pika.PlainCredentials(username, password)
        self.__host = host
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__host, credentials=self.__user_credentials)
        )
        self.channel = self.connection.channel()

    def basic_properties(self, reply_to: str, correlation_id: str):
        return pika.BasicProperties(reply_to=reply_to, correlation_id=correlation_id)
