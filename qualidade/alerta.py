import logging
import os

import requests

log = logging.getLogger(__name__)


class Alerta:
    def __init__(self, token=None, chat=None, ambiente=None):
        self.token = token or os.getenv("telegram_token")
        self.chat = chat or os.getenv("telegram_chat")
        self.ambiente = ambiente or os.getenv("ambiente", "local")

    def configurado(self):
        return bool(self.token and self.chat)

    def enviar(self, mensagem):
        texto = f"[{self.ambiente}] {mensagem}"

        if not self.configurado():
            log.warning("alerta sem canal configurado: %s", texto)
            return False

        resposta = requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            json={"chat_id": self.chat, "text": texto},
            timeout=15,
        )
        resposta.raise_for_status()
        return True

    def mensagem_de_falha(self, contexto):
        tarefa = contexto["task_instance"]
        erro = contexto.get("exception")
        return (
            f"falha em {tarefa.dag_id}.{tarefa.task_id}\n"
            f"execucao: {tarefa.run_id}\n"
            f"tentativa: {tarefa.try_number}\n"
            f"erro: {erro}"
        )

    def falha(self, contexto):
        self.enviar(self.mensagem_de_falha(contexto))
