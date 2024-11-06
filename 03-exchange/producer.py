from rabbitmq_config import channel, connection_rmq


messages = [
    {
        "severity": "error",
        "msg": "Erro ao abrir o arquivo",
    },
    {
        "severity": "error",
        "msg": "Erro ao abrir o arquivo",
    },
    {
        "severity": "warn",
        "msg": "Falha na atualização de pacote",
    },
    {
        "severity": "critical",
        "msg": "System Will Explode!",
    },
    {
        "severity": "warn",
        "msg": "Atualize seus pacotes",
    },
]


def set_routing_key(severity: str):
    return "critical_logs" if severity == "critical" else "general_logs"


channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

for msg in messages:
    channel.basic_publish(
        exchange="direct_logs",
        routing_key=set_routing_key(msg["severity"]),
        body=msg["msg"],
    )

    print(f"The message: {msg['msg']} with severity: {msg['severity']} was sent")

connection_rmq.close()
