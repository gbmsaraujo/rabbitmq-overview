from producer import OperationsRpcClientProducer
from client_consumer import ClientOperationConsumer
from config import RabbitMQConfig


rmq = RabbitMQConfig()

operations_rpc_producer = OperationsRpcClientProducer(
    exchange_name="rpc_exchange",
    exchange_type="direct",
    routing_key="rpc_queue_bind",
    rmq=rmq,
)

correlation_id, reply_to = operations_rpc_producer.send_request(5)

client_consumer = ClientOperationConsumer(correlation_id, reply_to, rmq=rmq)

client_consumer.wait_for_response()
