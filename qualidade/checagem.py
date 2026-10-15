class Checagem:
    def __init__(self, nome, arquivo_sql, severidade, descricao):
        self.nome = nome
        self.arquivo_sql = arquivo_sql
        self.severidade = severidade
        self.descricao = descricao


checagens = [
    Checagem("posto_com_duas_versoes_atuais", "posto_com_duas_versoes_atuais.sql", "critica",
             "um posto nao pode ter mais de uma versao atual na dim_posto"),
    Checagem("vigencia_sobreposta", "vigencia_sobreposta.sql", "critica",
             "as versoes de um mesmo posto nao podem se sobrepor no tempo"),
    Checagem("preco_invalido_na_fato", "preco_invalido_na_fato.sql", "critica",
             "a fato nao pode ter preco vazio, zerado ou negativo"),
    Checagem("rejeitados_acima_do_limite", "rejeitados_acima_do_limite.sql", "aviso",
             "mais de 5% das linhas do arquivo foram para a quarentena"),
    Checagem("variacao_de_volume", "variacao_de_volume.sql", "aviso",
             "o volume do arquivo variou mais de 30% em relacao a media dos ultimos 4"),
    Checagem("dados_desatualizados", "dados_desatualizados.sql", "aviso",
             "a coleta mais recente tem mais de 15 dias"),
]
