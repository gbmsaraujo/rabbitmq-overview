logs_queues = [
    {"bind": "critical_log_bind", "queue": "critical_log_queue"},
    {"bind": "general_log_bind", "queue": "general_log_queue"},
]


logs_messages = [
    {"severity": "critical", "msg": "Falha no banco"},
    {"severity": "info", "msg": "Operação concluída com sucesso"},
    {"severity": "error", "msg": "Erro de autenticação"},
    {"severity": "info", "msg": "Registro adicionado ao banco de dados"},
    {"severity": "error", "msg": "Conexão perdida com o servidor"},
    {"severity": "critical", "msg": "Sistema indisponível"},
    {"severity": "info", "msg": "Atualização de software disponível"},
    {"severity": "error", "msg": "Recurso não encontrado"},
    {"severity": "critical", "msg": "Erro interno no servidor"},
    {"severity": "info", "msg": "Usuário conectado"},
]

ROUTING_LOG_KEY = "logs_key"
