logs_queues = [
    {"bind": "*.critical", "queue": "critical_log_topic"},
    {"bind": "log.*", "queue": "general_log_topic"},
]


logs_messages = [
    {"severity": "log.critical", "msg": "Falha no banco"},
    {"severity": "log.info", "msg": "Operação concluída com sucesso"},
    {"severity": "log.error", "msg": "Erro de autenticação"},
    {"severity": "log.info", "msg": "Registro adicionado ao banco de dados"},
    {"severity": "log.error", "msg": "Conexão perdida com o servidor"},
    {"severity": "log.critical", "msg": "Sistema indisponível"},
    {"severity": "log.info", "msg": "Atualização de software disponível"},
    {"severity": "log.error", "msg": "Recurso não encontrado"},
    {"severity": "log.critical", "msg": "Erro interno no servidor"},
    {"severity": "log.info", "msg": "Usuário conectado"},
]
