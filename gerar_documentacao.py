from qualidade.documentacao import GeradorDocumentacao

if __name__ == "__main__":
    total = GeradorDocumentacao("processos").gerar("docs/processos.md")
    print(f"{total} processo(s) documentado(s) em docs/processos.md")
