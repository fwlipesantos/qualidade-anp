import logging
import os

from qualidade.checagem import checagens

log = logging.getLogger(__name__)


class FalhaQualidade(Exception):
    pass


class VerificadorQualidade:
    def __init__(self, banco, pasta_sql, alerta=None):
        self.banco = banco
        self.pasta = os.path.join(pasta_sql, "checagens")
        self.alerta = alerta

    def ler_sql(self, checagem):
        with open(os.path.join(self.pasta, checagem.arquivo_sql), encoding="utf-8") as arquivo:
            return arquivo.read().strip()

    def executar_checagem(self, checagem, arquivo):
        comando = self.ler_sql(checagem)
        parametros = {}
        if ":arquivo" in comando:
            parametros["arquivo"] = arquivo
        linhas = self.banco.consultar(comando, parametros)
        return int(linhas[0][0] or 0)

    def executar(self, arquivo):
        criticas = []
        avisos = []

        for checagem in checagens:
            problemas = self.executar_checagem(checagem, arquivo)
            self.registrar(arquivo, checagem, problemas)

            if problemas == 0:
                log.info("ok: %s", checagem.nome)
                continue

            log.warning("%s: %s problema(s) - %s", checagem.nome, problemas, checagem.descricao)
            if checagem.severidade == "critica":
                criticas.append(checagem.nome)
            else:
                avisos.append(checagem.nome)

        self.banco.confirmar()

        if avisos and self.alerta:
            self.alerta.enviar(f"avisos de qualidade em {arquivo}: " + ", ".join(avisos))

        if criticas:
            raise FalhaQualidade(f"checagens criticas falharam em {arquivo}: " + ", ".join(criticas))

        return {"criticas": criticas, "avisos": avisos}

    def registrar(self, arquivo, checagem, problemas):
        self.banco.executar(
            """
            insert into resultado_qualidade (arquivo, checagem, severidade, problemas, aprovado)
            values (:arquivo, :checagem, :severidade, :problemas, :aprovado)
            """,
            {
                "arquivo": arquivo,
                "checagem": checagem.nome,
                "severidade": checagem.severidade,
                "problemas": problemas,
                "aprovado": "S" if problemas == 0 else "N",
            },
        )
