import os

import yaml


class GeradorDocumentacao:
    campos = ["nome", "finalidade", "origem", "destino", "janela", "responsavel"]

    def __init__(self, pasta_processos):
        self.pasta = pasta_processos

    def ler_fichas(self):
        fichas = []
        for nome in sorted(os.listdir(self.pasta)):
            if not nome.endswith(".yml"):
                continue
            with open(os.path.join(self.pasta, nome), encoding="utf-8") as arquivo:
                ficha = yaml.safe_load(arquivo)
            faltando = [campo for campo in self.campos if not ficha.get(campo)]
            if faltando:
                raise ValueError(f"ficha {nome} sem os campos: " + ", ".join(faltando))
            fichas.append(ficha)
        return fichas

    def gerar(self, destino):
        fichas = self.ler_fichas()
        linhas = ["# processos", ""]

        for ficha in fichas:
            linhas.append(f"## {ficha['nome']}")
            linhas.append("")
            linhas.append(f"**finalidade:** {ficha['finalidade']}")
            linhas.append("")
            linhas.append(f"**janela de execucao:** {ficha['janela']}")
            linhas.append("")
            linhas.append(f"**responsavel:** {ficha['responsavel']}")
            linhas.append("")
            linhas.append("**origem:** " + ", ".join(ficha["origem"]))
            linhas.append("")
            linhas.append("**destino:** " + ", ".join(ficha["destino"]))
            linhas.append("")
            linhas.append("```mermaid")
            linhas.append("flowchart LR")
            for origem in ficha["origem"]:
                for alvo in ficha["destino"]:
                    linhas.append(f'    "{origem}" --> "{alvo}"')
            linhas.append("```")
            linhas.append("")

        os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
        with open(destino, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas))
        return len(fichas)
