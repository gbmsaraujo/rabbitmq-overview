import pika

# A conexão (connection) é a camada de comunicação entre o cliente e o servidor RabbitMQ. É através da conexão que o cliente estabelece a comunicação e troca mensagens com o servidor RabbitMQ. A conexão é responsável por estabelecer uma conexão TCP/IP com o servidor RabbitMQ e fornecer uma interface para a criação de canais.
connection_rmq = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

# O canal (channel) é uma abstração dentro da conexão que permite realizar operações específicas, como declarar filas, criar bindings, publicar e consumir mensagens. É através do canal que você realiza as principais interações com o RabbitMQ.
channel = connection_rmq.channel()
