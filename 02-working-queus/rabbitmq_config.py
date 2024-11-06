import pika

connection_parameters = pika.ConnectionParameters("localhost")

connection_rmq = pika.BlockingConnection(connection_parameters)

channel = connection_rmq.channel()
