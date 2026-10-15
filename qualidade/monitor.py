import logging
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class MonitorAtraso:
    def __init__(self, banco, alerta):
        self.banco = banco
        self.alerta = alerta

    def ultima_carga(self):
        linhas = self.banco.consultar("select max(fim) from controle_arquivo where status = 'sucesso'")
        return linhas[0][0]

    def verificar(self, processo, limite_horas, agora=None):
        agora = agora or datetime.now()
        ultima = self.ultima_carga()

        if ultima is None:
            self.alerta.enviar(f"{processo}: nenhuma carga com sucesso registrada")
            return False

        atraso = agora - ultima
        if atraso > timedelta(hours=limite_horas):
            horas = int(atraso.total_seconds() // 3600)
            self.alerta.enviar(f"{processo}: ultima carga com sucesso ha {horas} horas, limite de {limite_horas}")
            return False

        log.info("%s em dia, ultima carga em %s", processo, ultima)
        return True
