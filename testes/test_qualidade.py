from datetime import datetime

import pytest

from qualidade.alerta import Alerta
from qualidade.documentacao import GeradorDocumentacao
from qualidade.monitor import MonitorAtraso
from qualidade.verificador import FalhaQualidade, VerificadorQualidade


class BancoFalso:
    def __init__(self, respostas=None, padrao=0):
        self.respostas = respostas or {}
        self.padrao = padrao
        self.registros = []
        self.parametros = []

    def consultar(self, comando, parametros=None):
        self.parametros.append(parametros)
        for trecho, valor in self.respostas.items():
            if trecho in comando:
                return [(valor,)]
        return [(self.padrao,)]

    def executar(self, comando, parametros=None):
        self.registros.append(parametros)

    def confirmar(self):
        pass


class AlertaFalso:
    def __init__(self):
        self.mensagens = []

    def enviar(self, mensagem):
        self.mensagens.append(mensagem)


def test_tudo_aprovado():
    banco = BancoFalso()
    resultado = VerificadorQualidade(banco, "sql").executar("ca-2024-01.csv")
    assert resultado == {"criticas": [], "avisos": []}
    assert len(banco.registros) == 6


def test_aviso_gera_alerta_sem_interromper():
    alerta = AlertaFalso()
    banco = BancoFalso({"0.05 *": 1})
    resultado = VerificadorQualidade(banco, "sql", alerta).executar("ca-2024-01.csv")
    assert resultado["avisos"] == ["rejeitados_acima_do_limite"]
    assert "rejeitados_acima_do_limite" in alerta.mensagens[0]


def test_checagem_critica_interrompe():
    banco = BancoFalso({"atual = 'S'": 2})
    with pytest.raises(FalhaQualidade):
        VerificadorQualidade(banco, "sql").executar("ca-2024-01.csv")


def test_arquivo_so_e_passado_quando_a_consulta_usa():
    banco = BancoFalso()
    VerificadorQualidade(banco, "sql").executar("ca-2024-01.csv")
    assert {} in banco.parametros
    assert {"arquivo": "ca-2024-01.csv"} in banco.parametros


def test_monitor_alerta_quando_atrasado():
    alerta = AlertaFalso()
    banco = BancoFalso({"max(fim)": datetime(2024, 1, 1)})
    em_dia = MonitorAtraso(banco, alerta).verificar("precos_anp", 192, agora=datetime(2024, 1, 20))
    assert not em_dia
    assert "456 horas" in alerta.mensagens[0]


def test_monitor_em_dia():
    alerta = AlertaFalso()
    banco = BancoFalso({"max(fim)": datetime(2024, 1, 19)})
    assert MonitorAtraso(banco, alerta).verificar("precos_anp", 192, agora=datetime(2024, 1, 20))
    assert alerta.mensagens == []


def test_alerta_sem_canal_nao_quebra():
    assert Alerta(token="", chat="", ambiente="dev").enviar("teste") is False


def test_documentacao_gerada(tmp_path):
    destino = tmp_path / "processos.md"
    total = GeradorDocumentacao("processos").gerar(str(destino))
    texto = destino.read_text(encoding="utf-8")
    assert total == 2
    assert "precos_anp" in texto
    assert "flowchart LR" in texto


def test_ficha_incompleta_e_recusada(tmp_path):
    (tmp_path / "ruim.yml").write_text("nome: x\nfinalidade: y\n", encoding="utf-8")
    with pytest.raises(ValueError):
        GeradorDocumentacao(str(tmp_path)).ler_fichas()
